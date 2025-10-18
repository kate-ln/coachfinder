import sqlite3
import secrets
from flask import Flask
from flask import redirect, render_template, request, session, make_response, abort, flash
from werkzeug.security import check_password_hash, generate_password_hash
import markupsafe
import config
import ui
import announcements_student
import announcements_coach
import users
import messages

app = Flask(__name__)
app.secret_key = config.secret_key
app.debug = True

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

def require_login():
    if "user_id" not in session:
        return ui.handle_login_required()
    return None

def ensure_csrf_token():
    """Ensure user has a CSRF token in their session"""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)

def check_csrf():
    """Check CSRF token to prevent CSRF attacks"""
    if "csrf_token" not in session:
        abort(403)
    if request.form.get("csrf_token") != session["csrf_token"]:
        abort(403)

def get_form_options():
    classes = announcements_student.get_all_classes()
    age_groups = [{"value": value, "label": value} for value in classes.get("Ikäryhmä", [])]
    skill_levels = [{"value": value, "label": value} for value in classes.get("Taitotaso", [])]
    return age_groups, skill_levels

def validate_announcement_form(sport, city, age_group, skill_level, description):
    """Validate announcement form data and return error message if invalid"""
    if not sport:
        return "VIRHE: Laji on pakollinen"
    if not city:
        return "VIRHE: Kaupunki on pakollinen"
    if not age_group:
        return "VIRHE: Ikäryhmä on pakollinen"
    if not skill_level:
        return "VIRHE: Taitotaso on pakollinen"
    if not description:
        return "VIRHE: Kuvaus on pakollinen"
    if len(sport) > 50:
        return "VIRHE: Laji on liian pitkä (max 50 merkkiä)"
    if len(city) > 50:
        return "VIRHE: Kaupunki on liian pitkä (max 50 merkkiä)"
    if len(description) > 1000:
        return "VIRHE: Kuvaus on liian pitkä (max 1000 merkkiä)"
    return None

def validate_announcement_selectors(age_group, skill_level, age_groups, skill_levels):
    """Validate age group and skill level selectors"""
    valid_age_groups = [option["value"] for option in age_groups]
    valid_skill_levels = [option["value"] for option in skill_levels]
    if age_group not in valid_age_groups:
        return "VIRHE: virheellinen ikäryhmä"
    if skill_level not in valid_skill_levels:
        return "VIRHE: virheellinen taitotaso"
    return None

def render_announcement_form_with_error(error_message, sport, city, age_group,
                                        skill_level, description):
    """Render announcement form with error message and filled data"""
    age_groups, skill_levels = get_form_options()
    filled = {"sport": sport, "city": city, "age_group": age_group,
             "skill_level": skill_level, "description": description}
    flash(error_message)
    return render_template("create_announcement_student.html",
                         classes=announcements_student.get_all_classes(),
                         age_groups=age_groups,
                         skill_levels=skill_levels,
                         filled=filled)

def render_edit_announcement_form_with_error(error_message, announcement_id,
                                              sport, city, age_group, skill_level,
                                              description):
    """Render edit announcement form with error message and filled data"""
    age_groups, skill_levels = get_form_options()
    classes = announcements_student.get_classes(announcement_id)
    filled = {"sport": sport, "city": city, "age_group": age_group,
             "skill_level": skill_level, "description": description}
    flash(error_message)
    return render_template("edit_announcement.html",
                         announcement={"id": announcement_id, **filled},
                         classes=classes,
                         age_groups=age_groups,
                         skill_levels=skill_levels)

def validate_coach_announcement_form(sport, city, experience_level, description):
    """Validate coach announcement form data and return error message if invalid"""
    if not sport:
        return "VIRHE: Laji on pakollinen"
    if not city:
        return "VIRHE: Paikkakunta on pakollinen"
    if not experience_level:
        return "VIRHE: Kokemus on pakollinen"
    if not description:
        return "VIRHE: Kuvaus on pakollinen"
    if len(sport) > 50:
        return "VIRHE: Laji on liian pitkä (max 50 merkkiä)"
    if len(city) > 50:
        return "VIRHE: Paikkakunta on liian pitkä (max 50 merkkiä)"
    if len(description) > 1000:
        return "VIRHE: Kuvaus on liian pitkä (max 1000 merkkiä)"
    return None

def render_coach_announcement_form_with_error(error_message, sport, city,
                                              experience_level, description):
    """Render coach announcement form with error message and filled data"""
    classes = announcements_coach.get_all_classes()
    experience_levels = [{"value": value, "label": value} for value in classes.get("Kokemus", [])]
    filled = {"sport": sport, "city": city, "experience_level": experience_level,
             "description": description}
    flash(error_message)
    return render_template("create_announcement_coach.html",
                         classes=classes,
                         experience_levels=experience_levels,
                         filled=filled)

def render_edit_coach_announcement_form_with_error(error_message, announcement_id,
                                                   sport, city, experience_level,
                                                   description):
    """Render edit coach announcement form with error message and filled data"""
    classes = announcements_coach.get_all_classes()
    experience_levels = [{"value": value, "label": value} for value in classes.get("Kokemus", [])]
    filled = {"sport": sport, "city": city, "experience_level": experience_level,
             "description": description}
    flash(error_message)
    return render_template("edit_announcement_coach.html",
                         announcement={"id": announcement_id, **filled},
                         classes=classes,
                         experience_levels=experience_levels)

@app.route("/")
def index():
    student_announcements = announcements_student.get_announcements()
    coach_announcements = announcements_coach.get_announcements()
    profile = None
    if "user_id" in session:
        user_data = users.get_user_profile(session["user_id"])
        if user_data:
            profile = user_data[0]
    return render_template("index.html", 
                         student_announcements=student_announcements,
                         coach_announcements=coach_announcements,
                         profile=profile)

@app.route("/choose_announcement_type")
def choose_announcement_type():
    login_check = require_login()
    if login_check:
        return login_check
    ensure_csrf_token()
    return render_template("choose_announcement_type.html")

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
    classes = announcements_student.get_classes(announcement_id)
    return render_template("show_announcement.html", announcement=a, classes=classes)

@app.route("/create_announcement_student", methods=["GET", "POST"])
def create_announcement_student():
    login_check = require_login()
    if login_check:
        return login_check
    if request.method == "GET":
        ensure_csrf_token()
        age_groups, skill_levels = get_form_options()
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled={})
    check_csrf()
    sport = request.form.get("sport", "").strip()
    city = request.form.get("city", "").strip()
    age_group = request.form.get("age_group", "").strip()
    skill_level = request.form.get("skill_level", "").strip()
    description = request.form.get("description", "").strip()
    error_message = validate_announcement_form(sport, city, age_group, skill_level, description)
    if error_message:
        return render_announcement_form_with_error(error_message, sport, city,
                                                   age_group, skill_level, description)
    age_groups, skill_levels = get_form_options()
    selector_error = validate_announcement_selectors(age_group, skill_level,
                                                     age_groups, skill_levels)
    if selector_error:
        return render_announcement_form_with_error(selector_error, sport, city,
                                                   age_group, skill_level, description)

    user_id = session["user_id"]
    if age_group and announcements_student.check_age_group_conflict(user_id, age_group):
        session['pending_announcement'] = {
            'sport': sport,
            'city': city,
            'age_group': age_group,
            'skill_level': skill_level,
            'description': description
        }
        return redirect("/confirm_age_group_change")
    
    announcements_student.add_announcement(sport, city, age_group, skill_level,
                                           description, user_id)
    flash("Ilmoitus luotu onnistuneesti")
    return redirect("/")

@app.route("/confirm_age_group_change", methods=["GET", "POST"])
def confirm_age_group_change():
    login_check = require_login()
    if login_check:
        return login_check
    
    if request.method == "GET":
        ensure_csrf_token()
        pending_announcement = session.get('pending_announcement')
        if not pending_announcement:
            flash("Virhe: Ei odottavaa ilmoitusta löytynyt.")
            return redirect("/create_announcement_student")
        return render_template("confirm_age_group_change.html", 
                             pending_announcement=pending_announcement)
    
    check_csrf()
    confirm = request.form.get("confirm")
    pending_announcement = session.get('pending_announcement')
    
    if not pending_announcement:
        flash("Virhe: Ei odottavaa ilmoitusta löytynyt.")
        return redirect("/create_announcement_student")
    
    user_id = session["user_id"]
    
    if confirm == "yes":
        announcements_student.update_all_user_age_groups(user_id, pending_announcement['age_group'])
        
        announcements_student.add_announcement(
            pending_announcement['sport'],
            pending_announcement['city'],
            pending_announcement['age_group'],
            pending_announcement['skill_level'],
            pending_announcement['description'],
            user_id
        )
        
        session.pop('pending_announcement', None)
        flash("Ikäryhmä päivitetty ja ilmoitus luotu onnistuneesti")
        return redirect("/")
    else:
        session.pop('pending_announcement', None)
        age_groups, skill_levels = get_form_options()
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=pending_announcement)

@app.route("/confirm_age_group_change_update", methods=["GET", "POST"])
def confirm_age_group_change_update():
    login_check = require_login()
    if login_check:
        return login_check
    
    if request.method == "GET":
        ensure_csrf_token()
        pending_update = session.get('pending_update')
        if not pending_update:
            flash("Virhe: Ei odottavaa päivitystä löytynyt.")
            return redirect("/")
        return render_template("confirm_age_group_change_update.html", 
                             pending_update=pending_update)
    
    check_csrf()
    confirm = request.form.get("confirm")
    pending_update = session.get('pending_update')
    
    if not pending_update:
        flash("Virhe: Ei odottavaa päivitystä löytynyt.")
        return redirect("/")
    
    user_id = session["user_id"]
    
    if confirm == "yes":
        announcements_student.update_all_user_age_groups(user_id, pending_update['age_group'])
        
        announcements_student.update_announcement(
            pending_update['announcement_id'],
            pending_update['sport'],
            pending_update['city'],
            pending_update['age_group'],
            pending_update['skill_level'],
            pending_update['description']
        )
        
        session.pop('pending_update', None)
        flash("Ikäryhmä päivitetty ja ilmoitus muokattu onnistuneesti")
        return redirect(f"/announcement/{pending_update['announcement_id']}")
    else:
        session.pop('pending_update', None)
        flash("Ilmoituksen muokkaus peruutettu")
        return redirect(f"/announcement/{pending_update['announcement_id']}")

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
    classes = announcements_student.get_classes(announcement_id)
    age_groups, skill_levels = get_form_options()
    ensure_csrf_token()
    return render_template("edit_announcement.html",
                         announcement=a,
                         classes=classes,
                         age_groups=age_groups,
                         skill_levels=skill_levels)

@app.route("/update_announcement_student", methods=["GET", "POST"])
def update_announcement_student():
    login_check = require_login()
    if login_check:
        return login_check
    if request.method == "GET":
        ensure_csrf_token()
        return render_template("create_announcement_student.html")
    check_csrf()
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

    # Validate form data
    error_message = validate_announcement_form(sport, city, age_group, skill_level, description)
    if error_message:
        return render_edit_announcement_form_with_error(error_message, announcement_id,
                                                        sport, city, age_group, skill_level,
                                                        description)

    # Get form options for validation
    age_groups, skill_levels = get_form_options()
    selector_error = validate_announcement_selectors(age_group, skill_level,
                                                     age_groups, skill_levels)
    if selector_error:
        return render_edit_announcement_form_with_error(selector_error, announcement_id,
                                                        sport, city, age_group, skill_level,
                                                        description)

    user_id = session["user_id"]
    
    if age_group and announcements_student.check_age_group_conflict_excluding(user_id, age_group, announcement_id):
        session['pending_update'] = {
            'announcement_id': announcement_id,
            'sport': sport,
            'city': city,
            'age_group': age_group,
            'skill_level': skill_level,
            'description': description
        }
        return redirect("/confirm_age_group_change_update")
    
    announcements_student.update_announcement(announcement_id, sport, city,
                                               age_group, skill_level, description)
    flash("Ilmoitus päivitetty onnistuneesti")
    return redirect(f"/announcement/{announcement_id}")

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
        ensure_csrf_token()
        return render_template("remove_announcement.html", announcement=a)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            announcements_student.remove_announcement(announcement_id)
            flash("Ilmoitus poistettu onnistuneesti")
            return redirect("/")
        return redirect(f"/announcement/{announcement_id}")

# Coach announcement routes
@app.route("/create_announcement_coach", methods=["GET", "POST"])
def create_announcement_coach():
    login_check = require_login()
    if login_check:
        return login_check
    if request.method == "GET":
        ensure_csrf_token()
        classes = announcements_coach.get_all_classes()
        experience_levels = [{"value": value, "label": value} for value in classes.get("Kokemus", [])]
        return render_template("create_announcement_coach.html",
                             classes=classes,
                             experience_levels=experience_levels,
                             filled={})
    check_csrf()
    sport = request.form.get("sport", "").strip()
    city = request.form.get("city", "").strip()
    experience_level = request.form.get("experience_level", "").strip()
    description = request.form.get("description", "").strip()
    
    # Validate form data
    error_message = validate_coach_announcement_form(sport, city, experience_level, description)
    if error_message:
        return render_coach_announcement_form_with_error(error_message, sport, city,
                                                         experience_level, description)
    
    # Validate experience level selector
    classes = announcements_coach.get_all_classes()
    experience_levels = [option["value"] for option in [{"value": value, "label": value} for value in classes.get("Kokemus", [])]]
    
    if experience_level not in experience_levels:
        return render_coach_announcement_form_with_error("VIRHE: virheellinen kokemus", sport, city,
                                                         experience_level, description)

    user_id = session["user_id"]
    announcements_coach.add_announcement(sport, city, experience_level, description, user_id)
    flash("Valmentajailmoitus luotu onnistuneesti")
    return redirect("/")

@app.route("/announcement_coach/<int:announcement_id>")
def show_announcement_coach(announcement_id):
    a = announcements_coach.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    classes = announcements_coach.get_classes(announcement_id)
    return render_template("show_announcement_coach.html", announcement=a, classes=classes)

@app.route("/edit_announcement_coach/<int:announcement_id>")
def edit_announcement_coach(announcement_id):
    login_check = require_login()
    if login_check:
        return login_check
    a = announcements_coach.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    if a["user_id"] != session["user_id"]:
        return ui.handle_announcement_forbidden("muokata")
    classes = announcements_coach.get_all_classes()
    experience_levels = [{"value": value, "label": value} for value in classes.get("Kokemus", [])]
    ensure_csrf_token()
    return render_template("edit_announcement_coach.html",
                         announcement=a,
                         classes=classes,
                         experience_levels=experience_levels)

@app.route("/update_announcement_coach", methods=["GET", "POST"])
def update_announcement_coach():
    login_check = require_login()
    if login_check:
        return login_check
    if request.method == "GET":
        ensure_csrf_token()
        return render_template("create_announcement_coach.html")
    check_csrf()
    announcement_id = request.form["announcement_id"]
    a = announcements_coach.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    if a["user_id"] != session["user_id"]:
        return ui.handle_announcement_forbidden("päivittää")
    sport = request.form.get("sport", "").strip()
    city = request.form.get("city", "").strip()
    experience_level = request.form.get("experience_level", "").strip()
    description = request.form.get("description", "").strip()

    # Validate form data
    error_message = validate_coach_announcement_form(sport, city, experience_level, description)
    if error_message:
        return render_edit_coach_announcement_form_with_error(error_message, announcement_id,
                                                              sport, city, experience_level, description)

    # Validate experience level selector
    classes = announcements_coach.get_all_classes()
    experience_levels = [option["value"] for option in [{"value": value, "label": value} for value in classes.get("Kokemus", [])]]
    
    if experience_level not in experience_levels:
        return render_edit_coach_announcement_form_with_error("VIRHE: virheellinen kokemus", announcement_id,
                                                              sport, city, experience_level, description)
    
    announcements_coach.update_announcement(announcement_id, sport, city, experience_level, description)
    flash("Valmentajailmoitus päivitetty onnistuneesti")
    return redirect(f"/announcement_coach/{announcement_id}")

@app.route("/remove_announcement_coach/<int:announcement_id>", methods=["GET", "POST"])
def remove_announcement_coach(announcement_id):
    login_check = require_login()
    if login_check:
        return login_check
    a = announcements_coach.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    if a["user_id"] != session["user_id"]:
        return ui.handle_announcement_forbidden("poistaa")
    if request.method == "GET":
        ensure_csrf_token()
        return render_template("remove_announcement_coach.html", announcement=a)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            announcements_coach.remove_announcement(announcement_id)
            flash("Valmentajailmoitus poistettu onnistuneesti")
            return redirect("/")
        return redirect(f"/announcement_coach/{announcement_id}")

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

def validate_message_form(recipient_username, body):
    """Validate message form data and return error message if invalid"""
    if not recipient_username or not body:
        return "VIRHE: vastaanottaja ja viesti ovat pakollisia"
    if len(body) > 2000:
        return "VIRHE: viesti on liian pitkä (max 2000 merkkiä)"
    return None

def render_message_form_with_error(error_message, recipient_username, body):
    """Render message form with error message and filled data"""
    flash(error_message)
    filled = {"recipient": recipient_username, "body": body}
    return render_template("message_new.html", filled=filled)

@app.route("/messages/new", methods=["GET", "POST"])
def message_new():
    login_check = require_login()
    if login_check:
        return login_check
    if request.method == "GET":
        ensure_csrf_token()
        return render_template("message_new.html", filled={})
    check_csrf()
    me = session["user_id"]
    recipient_username = request.form.get("recipient", "").strip()
    body = request.form.get("body", "").strip()

    # Validate form data
    error_message = validate_message_form(recipient_username, body)
    if error_message:
        return render_message_form_with_error(error_message, recipient_username, body)

    # Check if recipient exists
    rec = users.find_user_id_by_username(recipient_username)
    if not rec:
        return render_message_form_with_error("VIRHE: vastaanottajaa ei löydy",
                                              recipient_username, body)

    other_id = rec["id"]
    if other_id == me:
        return render_message_form_with_error("VIRHE: et voi lähettää viestiä itsellesi",
                                              recipient_username, body)

    thread_id = _find_or_create_thread(me, other_id)
    messages.add_message(thread_id, me, body)
    flash("Viesti lähetetty onnistuneesti")
    return redirect(f"/messages/{thread_id}")

@app.route("/messages/<int:thread_id>", methods=["GET", "POST"])
def messages_thread(thread_id: int):
    login_check = require_login()
    if login_check:
        return login_check
    me = session["user_id"]
    t = messages.get_thread_participants(thread_id)
    if not t:
        return ui.handle_thread_not_found()
    a, b = t[0]["user_a_id"], t[0]["user_b_id"]
    if me not in (a, b):
        return ui.handle_thread_access_denied()
    if request.method == "POST":
        check_csrf()
        body = request.form.get("body", "").strip()
        if not body:
            flash("VIRHE: viesti ei voi olla tyhjä")
            return redirect(f"/messages/{thread_id}")
        if len(body) > 2000:
            flash("VIRHE: viesti on liian pitkä (max 2000 merkkiä)")
            return redirect(f"/messages/{thread_id}")
        messages.add_message(thread_id, me, body)
        flash("Viesti lähetetty onnistuneesti")
        return redirect(f"/messages/{thread_id}")
    other_id = b if me == a else a
    other_user = users.get_user_by_id(other_id)
    msgs = messages.get_thread_messages(thread_id)
    ensure_csrf_token()
    return render_template("messages_thread.html", other_user=other_user,
                           messages=msgs, thread_id=thread_id)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})
    return None

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return redirect("/register")
    username = request.form.get("username", "").strip()
    if len(username) > 16:
        flash("VIRHE: Tunnus on liian pitkä (max 16 merkkiä)")
        filled = {"username": username}
        return render_template("register.html", filled=filled)
    password1 = request.form.get("password1", "")
    password2 = request.form.get("password2", "")
    if password1 != password2:
        flash("VIRHE: Antamasi salasanat eivät ole samat")
        filled = {"username": username}
        return render_template("register.html", filled=filled)
    password_hash = generate_password_hash(password1)
    try:
        users.create_user(username, password_hash)
        flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään")
        return redirect("/")
    except sqlite3.IntegrityError:
        flash("VIRHE: Valitsemasi tunnus on jo varattu")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        next_page = request.args.get("next_page", "/")
        return render_template("login.html", filled={}, next_page=next_page)
    # Note: No CSRF protection needed for login as user is not logged in yet
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    next_page = request.form.get("next_page", "/")
    rows = users.get_user_by_username(username)
    if not rows:
        flash("VIRHE: väärä tunnus tai salasana")
        filled = {"username": username}
        return render_template("login.html", filled=filled, next_page=next_page)
    row = rows[0]
    if check_password_hash(row["password_hash"], password):
        session["user_id"] = row["id"]
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect(next_page)
    flash("VIRHE: väärä tunnus tai salasana")
    filled = {"username": username}
    return render_template("login.html", filled=filled, next_page=next_page)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    '''Own profile page'''
    login_check = require_login()
    if login_check:
        return login_check
    user_id = session["user_id"]
    if request.method == "POST":
        check_csrf()
        display_name = request.form.get("display_name", "").strip()
        if len(display_name) > 50:
            flash("VIRHE: näyttönimi on liian pitkä (max 50 merkkiä)")
            return redirect("/profile")
        users.update_user_display_name(user_id, display_name)
        flash("Näyttönimi päivitetty onnistuneesti")
        return redirect("/profile")
    user_data = users.get_user_profile(user_id)
    current_display_name = user_data[0]["display_name"] if user_data else None
    user = users.get_user(user_id)
    student_announcements = announcements_student.get_announcements_by_user(user_id)
    coach_announcements = announcements_coach.get_announcements_by_user(user_id)
    
    # Get age distribution data
    age_distribution = announcements_student.get_age_distribution()
    user_age_group = announcements_student.get_user_age_group(user_id)
    
    # Calculate percentages
    total_users = sum(row['count'] for row in age_distribution)
    age_distribution_with_percentages = []
    user_percentage = 0
    
    for row in age_distribution:
        percentage = round((row['count'] / total_users * 100), 1) if total_users > 0 else 0
        age_distribution_with_percentages.append({
            'age_group': row['age_group'],
            'count': row['count'],
            'percentage': percentage
        })
        if row['age_group'] == user_age_group:
            user_percentage = percentage
    
    ensure_csrf_token()
    return render_template("profile.html", current_display_name=current_display_name,
                           user=user, student_announcements=student_announcements,
                           coach_announcements=coach_announcements,
                           age_distribution=age_distribution_with_percentages,
                           user_age_group=user_age_group,
                           user_percentage=user_percentage)

@app.route("/profile/<int:user_id>")
def user_profile(user_id):
    '''Profile page for other users'''
    login_check = require_login()
    if login_check:
        return login_check
    user_data = users.get_user_by_id(user_id)
    if not user_data:
        return ui.handle_user_not_found()
    user = users.get_user(user_id)
    user = dict(user)
    user['display_name'] = user_data['display_name']
    student_announcements = announcements_student.get_announcements_by_user(user_id)
    coach_announcements = announcements_coach.get_announcements_by_user(user_id)
    return render_template("user_profile.html", user=user, student_announcements=student_announcements, coach_announcements=coach_announcements)

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    login_check = require_login()
    if login_check:
        return login_check

    if request.method == "GET":
        ensure_csrf_token()
        return render_template("add_image.html")

    check_csrf()
    file = request.files["image"]
    if not file.filename.endswith(".jpg"):
        flash("VIRHE: Lähettämäsi tiedosto ei ole jpg-tiedosto")
        return redirect("/add_image")

    image = file.read()
    if len(image) > 100 * 1024:
        flash("VIRHE: Lähettämäsi tiedosto on liian suuri")
        return redirect("/add_image")

    user_id = session["user_id"]
    users.update_image(user_id, image)
    flash("Kuvan lisääminen onnistui")
    return redirect("/profile")

@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/confirm_delete_image")
def confirm_delete_image():
    login_check = require_login()
    if login_check:
        return login_check
    ensure_csrf_token()
    return render_template("confirm_delete_image.html")

@app.route("/delete_image", methods=["POST"])
def delete_image():
    login_check = require_login()
    if login_check:
        return login_check
    check_csrf()
    user_id = session["user_id"]
    users.delete_image(user_id)
    flash("Profiilikuva poistettu onnistuneesti")
    return redirect("/profile")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        if "csrf_token" in session:
            del session["csrf_token"]
    return redirect("/")
