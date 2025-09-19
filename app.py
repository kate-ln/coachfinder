# Käyttäjä pystyy rekisteröimään sovellukseen tunnuksen ja salasanan, jotka tallennetaan tietokantaan:
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, render_template_string
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
from ui import render_error_with_link, render_success_redirect_with_countdown
import announcements_student

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    announcements = announcements_student.get_announcements()
    return render_template("index.html", announcements=announcements)

@app.route("/create_announcement_student", methods=["GET", "POST"])
def create_announcement_student():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "GET":
        return render_template("create_announcement_student.html")
    # POST: create
    sport = request.form.get("sport", "").strip()
    city = request.form.get("city", "").strip()
    age_group = request.form.get("age_group", "").strip()
    skill_level = request.form.get("skill_level", "").strip()
    description = request.form.get("description", "").strip()
    user_id = session["user_id"]
    announcements_student.add_announcement(sport, city, age_group, skill_level, description, user_id)
    return redirect("/")

def _norm_pair(uid1: int, uid2: int):
    return (uid1, uid2) if uid1 < uid2 else (uid2, uid1)

def _find_or_create_thread(user_id: int, other_id: int):
    a, b = _norm_pair(user_id, other_id)
    # Try find existing
    rows = db.query("SELECT id FROM threads WHERE user_a_id = ? AND user_b_id = ?", [a, b])
    if rows:
        return rows[0]["id"]
    # Create
    db.execute("INSERT INTO threads (user_a_id, user_b_id) VALUES (?, ?)", [a, b])
    # Fetch id
    rows = db.query("SELECT id FROM threads WHERE user_a_id = ? AND user_b_id = ?", [a, b])
    return rows[0]["id"]

@app.route("/messages", methods=["GET"])
def messages_index():
    if "user_id" not in session:
        return redirect("/login")
    me = session["user_id"]

    # List threads I participate in with latest message preview
    sql = """
    SELECT
      t.id AS thread_id,
      CASE WHEN t.user_a_id = ? THEN u2.username ELSE u1.username END AS other_username,
      lm.body AS last_body,
      lm.created_at AS last_at
    FROM threads t
    JOIN users u1 ON u1.id = t.user_a_id
    JOIN users u2 ON u2.id = t.user_b_id
    JOIN (
      SELECT m1.thread_id, m1.body, m1.created_at
      FROM messages m1
      JOIN (
        SELECT thread_id, MAX(created_at) AS max_created_at
        FROM messages
        GROUP BY thread_id
      ) mm ON mm.thread_id = m1.thread_id AND mm.max_created_at = m1.created_at
    ) lm ON lm.thread_id = t.id
    WHERE t.user_a_id = ? OR t.user_b_id = ?
    ORDER BY lm.created_at DESC
    """
    rows = db.query(sql, [me, me, me])

    return render_template("messages_index.html", threads=rows)

@app.route("/messages/new", methods=["GET", "POST"])
def message_new():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "GET":
        return render_template("message_new.html")

    me = session["user_id"]
    recipient_username = request.form.get("recipient", "").strip()
    body = request.form.get("body", "").strip()

    if not recipient_username or not body:
        return "VIRHE: vastaanottaja ja viesti ovat pakollisia"

    rec = db.query("SELECT id FROM users WHERE username = ?", [recipient_username])
    if not rec:
        return "VIRHE: vastaanottajaa ei löydy"

    other_id = rec[0]["id"]
    if other_id == me:
        return "VIRHE: et voi lähettää viestiä itsellesi"

    thread_id = _find_or_create_thread(me, other_id)

    db.execute(
        "INSERT INTO messages (thread_id, sender_id, body) VALUES (?, ?, ?)",
        [thread_id, me, body]
    )
    return redirect(f"/messages/{thread_id}")

@app.route("/messages/<int:thread_id>", methods=["GET", "POST"])
def messages_thread(thread_id: int):
    if "user_id" not in session:
        return redirect("/login")
    me = session["user_id"]

    # Verify I’m a participant
    t = db.query("SELECT user_a_id, user_b_id FROM threads WHERE id = ?", [thread_id])
    if not t:
        return "VIRHE: keskustelua ei löydy"
    a, b = t[0]["user_a_id"], t[0]["user_b_id"]
    if me not in (a, b):
        return "VIRHE: ei käyttöoikeutta tähän keskusteluun"

    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if not body:
            return "VIRHE: viesti ei voi olla tyhjä"
        db.execute(
            "INSERT INTO messages (thread_id, sender_id, body) VALUES (?, ?, ?)",
            [thread_id, me, body]
        )
        return redirect(f"/messages/{thread_id}")

    # GET: show messages + the other user's name
    other_id = b if me == a else a
    other = db.query("SELECT username FROM users WHERE id = ?", [other_id])[0]["username"]

    msgs = db.query("""
        SELECT m.id, m.body, m.created_at, u.username AS sender
        FROM messages m
        JOIN users u ON u.id = m.sender_id
        WHERE m.thread_id = ?
        ORDER BY m.created_at ASC, m.id ASC
    """, [thread_id])

    return render_template("messages_thread.html", other_username=other, messages=msgs, thread_id=thread_id)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        # When a user clicks the back link, send them to the form page
        return redirect("/register")

    username  = request.form.get("username", "").strip()
    password1 = request.form.get("password1", "")
    password2 = request.form.get("password2", "")

    if password1 != password2:
        return render_error_with_link("VIRHE: salasanat eivät ole samat",
                                      "/create", "Palaa rekisteröitymiseen")

    password_hash = generate_password_hash(password1)
    try:
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                   [username, password_hash])
    except sqlite3.IntegrityError:
        return render_error_with_link("VIRHE: tunnus on jo varattu",
                                      "/create", "Palaa rekisteröitymiseen", status=409)

    return render_success_redirect_with_countdown("Tunnus luotu", seconds=5, href="/", link_text="Siirry heti")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    rows = db.query("SELECT id, password_hash FROM users WHERE username = ?", [username])
    if not rows:
        return render_error_with_link("VIRHE: väärä tunnus tai salasana",
                                      "/login", "Palaa kirjautumiseen", status=401)

    row = rows[0]
    if check_password_hash(row["password_hash"], password):
        session["user_id"] = row["id"]
        session["username"] = username
        return redirect("/")
    else:
        return render_error_with_link("VIRHE: väärä tunnus tai salasana",
                                      "/login", "Palaa kirjautumiseen", status=401)

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")