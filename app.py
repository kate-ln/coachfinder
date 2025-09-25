# Käyttäjä pystyy rekisteröimään sovellukseen tunnuksen ja salasanan, jotka tallennetaan tietokantaan:
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import ui
import announcements_student
import users
import messages

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        return ui.handle_login_required()
    return None

@app.route("/")
def index():
    a = announcements_student.get_announcements()
    profile = None
    if "user_id" in session:
        user_data = users.get_user_profile(session["user_id"])
        if user_data:
            profile = user_data[0]
    return render_template("index.html", announcements=a, profile=profile)

@app.route("/find_announcement")
def find_announcement():
    query = (request.args.get("query") or "").strip()
    results = announcements_student.find_announcements(query) if query else []
    return render_template("find_announcement.html", query=query, results=results)

@app.route("/announcement/<int:announcement_id>")
def show_announcement(announcement_id):
    a = announcements_student.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    return render_template("show_announcement.html", announcement=a)

@app.route("/create_announcement_student", methods=["GET", "POST"])
def create_announcement_student():
    login_check = require_login()
    if login_check:
        return login_check
    if request.method == "GET":
        return render_template("create_announcement_student.html")
    sport = request.form.get("sport", "").strip()
    city = request.form.get("city", "").strip()
    age_group = request.form.get("age_group", "").strip()
    skill_level = request.form.get("skill_level", "").strip()
    description = request.form.get("description", "").strip()
    user_id = session["user_id"]
    announcements_student.add_announcement(sport, city, age_group, skill_level, description, user_id)
    return redirect("/")

@app.route("/edit_announcement/<int:announcement_id>")
def edit_announcement(announcement_id):
    login_check = require_login()
    if login_check:
        return login_check
    a = announcements_student.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    if a["user_id"] != session["user_id"]:
        return ui.handle_announcement_forbidden("muokata")
    return render_template("edit_announcement.html", announcement=a)

@app.route("/update_announcement_student", methods=["GET", "POST"])
def update_announcement_student():
    login_check = require_login()
    if login_check:
        return login_check
    if request.method == "GET":
        return render_template("create_announcement_student.html")
    announcement_id = request.form["announcement_id"]
    a = announcements_student.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    if a["user_id"] != session["user_id"]:
        return ui.handle_announcement_forbidden("päivittää")
    sport = request.form.get("sport", "").strip()
    city = request.form.get("city", "").strip()
    age_group = request.form.get("age_group", "").strip()
    skill_level = request.form.get("skill_level", "").strip()
    description = request.form.get("description", "").strip()
    announcements_student.update_announcement(announcement_id, sport, city, age_group, skill_level, description)
    return redirect("/announcement/" + str(announcement_id))

@app.route("/remove_announcement/<int:announcement_id>", methods=["GET", "POST"])
def remove_announcement(announcement_id):
    login_check = require_login()
    if login_check:
        return login_check
    a = announcements_student.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    if a["user_id"] != session["user_id"]:
        return ui.handle_announcement_forbidden("poistaa")
    if request.method == "GET":
        return render_template("remove_announcement.html", announcement=a)
    if request.method == "POST":
        if "remove" in request.form:
            announcements_student.remove_announcement(announcement_id)
            return redirect("/")
        else:
            return redirect("/announcement/" + str(announcement_id))

def _norm_pair(uid1: int, uid2: int):
    return (uid1, uid2) if uid1 < uid2 else (uid2, uid1)

def _find_or_create_thread(user_id: int, other_id: int):
    a, b = _norm_pair(user_id, other_id)
    rows = messages.find_existing_thread(a, b)
    if rows:
        return rows[0]["id"]
    messages.create_thread(a, b)
    rows = messages.find_existing_thread(a, b)
    return rows[0]["id"]

@app.route("/messages", methods=["GET"])
def messages_index():
    login_check = require_login()
    if login_check:
        return login_check
    me = session["user_id"]
    rows = messages.get_user_threads(me)
    return render_template("messages_index.html", threads=rows)

@app.route("/messages/new", methods=["GET", "POST"])
def message_new():
    login_check = require_login()
    if login_check:
        return login_check
    if request.method == "GET":
        return render_template("message_new.html")
    me = session["user_id"]
    recipient_username = request.form.get("recipient", "").strip()
    body = request.form.get("body", "").strip()
    if not recipient_username or not body:
        return ui.handle_recipient_required_error()
    rec = users.find_user_id_by_username(recipient_username)
    if not rec:
        return ui.handle_recipient_not_found_error()
    other_id = rec["id"]
    if other_id == me:
        return ui.handle_self_message_error()
    thread_id = _find_or_create_thread(me, other_id)
    messages.add_message(thread_id, me, body)
    return redirect(f"/messages/{thread_id}")

@app.route("/messages/<int:thread_id>", methods=["GET", "POST"])
def messages_thread(thread_id: int):
    login_check = require_login()
    if login_check:
        return login_check
    me = session["user_id"]
    # Verify I'm a participant
    t = messages.get_thread_participants(thread_id)
    if not t:
        return ui.handle_thread_not_found()
    a, b = t[0]["user_a_id"], t[0]["user_b_id"]
    if me not in (a, b):
        return ui.handle_thread_access_denied()
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if not body:
            return ui.handle_empty_message_error()
        messages.add_message(thread_id, me, body)
        return redirect(f"/messages/{thread_id}")
    # GET: show messages + the other user's name
    other_id = b if me == a else a
    other_user = users.get_user_by_id(other_id)
    msgs = messages.get_thread_messages(thread_id)
    return render_template("messages_thread.html", other_user=other_user, messages=msgs, thread_id=thread_id)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return redirect("/register")
    username  = request.form.get("username", "").strip()
    password1 = request.form.get("password1", "")
    password2 = request.form.get("password2", "")
    if password1 != password2:
        return ui.handle_password_mismatch_error()
    password_hash = generate_password_hash(password1)
    try:
        users.create_user(username, password_hash)
    except sqlite3.IntegrityError:
        return ui.handle_duplicate_user_error()
    return ui.render_success_with_link("Tunnus luotu", href="/", link_text="Siirry etusivulle")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    rows = users.get_user_by_username(username)
    if not rows:
        return ui.handle_authentication_error()

    row = rows[0]
    if check_password_hash(row["password_hash"], password):
        session["user_id"] = row["id"]
        session["username"] = username
        return redirect("/")
    else:
        return ui.handle_authentication_error()

@app.route("/profile", methods=["GET", "POST"])
def profile():
    login_check = require_login()
    if login_check:
        return login_check
    user_id = session["user_id"]
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        if len(display_name) > 100:
            return ui.handle_display_name_too_long_error()
        users.update_user_display_name(user_id, display_name)
        return redirect("/profile")
    user_data = users.get_user_profile(user_id)
    current_display_name = user_data[0]["display_name"] if user_data else None
    return render_template("profile.html", current_display_name=current_display_name)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")