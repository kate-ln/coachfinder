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
import db

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

def get_coach_form_options():
    classes = announcements_coach.get_all_classes()
    experience_levels = [{"value": value, "label": value} for value in classes.get("Kokemus", [])]
    return experience_levels

def get_user_existing_age_group(user_id):
    """Get the age group from user's existing announcements, if any"""
    sql = "SELECT DISTINCT age_group FROM announcements_student WHERE user_id = ? AND age_group IS NOT NULL AND age_group != ''"
    result = db.query(sql, [user_id])
    if result:
        return result[0][0]  # Return the first (and should be only) age group
    return None

@app.route("/")
def index():
    # Get page number from query parameters, default to 1
    page = int(request.args.get('page', 1))
    page_size = 10  # Number of announcements per page
    
    # Get student announcements
    student_announcements = announcements_student.get_announcements()
    student_count = len(student_announcements)
    student_page_count = (student_count + page_size - 1) // page_size  # Ceiling division
    
    # Get coach announcements
    coach_announcements = announcements_coach.get_announcements()
    coach_count = len(coach_announcements)
    coach_page_count = (coach_count + page_size - 1) // page_size  # Ceiling division
    
    # Get user profile data
    user_profile_data = None
    if "user_id" in session:
        user_data = users.get_user_profile(session["user_id"])
        if user_data:
            user_profile_data = user_data[0]
    
    return render_template("index.html", 
                         student_announcements=student_announcements,
                         student_page_count=student_page_count,
                         coach_announcements=coach_announcements,
                         coach_page_count=coach_page_count,
                         page=page,
                         profile=user_profile_data)

@app.route("/find_announcement")
def find_announcement():
    query = (request.args.get("query") or "").strip()
    search_type = request.args.get("search_type", "students")
    active_only = request.args.get("active_only") == "1"
    
    results = []
    if query:
        if search_type == "coaches":
            results = announcements_coach.find_announcements(query, active_only)
        else:  # search_type == "students" or default
            results = announcements_student.find_announcements(query, active_only)
    
    return render_template("find_announcement.html", 
                         query=query, 
                         results=results, 
                         search_type=search_type, 
                         active_only=active_only)

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

    # Get form options for validation and template rendering
    age_groups, skill_levels = get_form_options()
    if not sport:
        flash("VIRHE: Laji on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=filled)
    if not city:
        flash("VIRHE: Kaupunki on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=filled)
    if not age_group:
        flash("VIRHE: Ikäryhmä on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=filled)
    if not skill_level:
        flash("VIRHE: Taitotaso on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=filled)
    if not description:
        flash("VIRHE: Kuvaus on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=filled)
    if len(sport) > 50:
        flash("VIRHE: Laji on liian pitkä (max 50 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=filled)
    if len(city) > 50:
        flash("VIRHE: Kaupunki on liian pitkä (max 50 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=filled)
    if len(description) > 1000:
        flash("VIRHE: Kuvaus on liian pitkä (max 1000 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=filled)
    # Validate that age_group and skill_level are from allowed options
    valid_age_groups = [option["value"] for option in age_groups]
    valid_skill_levels = [option["value"] for option in skill_levels]
    if age_group not in valid_age_groups:
        flash("VIRHE: virheellinen ikäryhmä")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=filled)
    if skill_level not in valid_skill_levels:
        flash("VIRHE: virheellinen taitotaso")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("create_announcement_student.html",
                             classes=announcements_student.get_all_classes(),
                             age_groups=age_groups,
                             skill_levels=skill_levels,
                             filled=filled)
    user_id = session["user_id"]
    
    # Check if user has existing announcements with different age group
    existing_age_group = get_user_existing_age_group(user_id)
    if existing_age_group and existing_age_group != age_group:
        # Store pending announcement in session and redirect to confirmation
        session["pending_announcement"] = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return redirect("/confirm_age_group_change")
    
    # No age group change, create announcement normally
    announcements_student.add_announcement(
        sport, city, age_group, skill_level, description, user_id)
    flash("Oppilasilmoitus luotu onnistuneesti")
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

    # Get form options for validation and template rendering
    age_groups, skill_levels = get_form_options()
    classes = announcements_student.get_classes(announcement_id)
    if not sport:
        flash("VIRHE: Laji on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("edit_announcement.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             age_groups=age_groups,
                             skill_levels=skill_levels)
    if not city:
        flash("VIRHE: Kaupunki on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("edit_announcement.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             age_groups=age_groups,
                             skill_levels=skill_levels)
    if not age_group:
        flash("VIRHE: Ikäryhmä on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("edit_announcement.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             age_groups=age_groups,
                             skill_levels=skill_levels)
    if not skill_level:
        flash("VIRHE: Taitotaso on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("edit_announcement.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             age_groups=age_groups,
                             skill_levels=skill_levels)
    if not description:
        flash("VIRHE: Kuvaus on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("edit_announcement.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             age_groups=age_groups,
                             skill_levels=skill_levels)

    if len(sport) > 50:
        flash("VIRHE: Laji on liian pitkä (max 50 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("edit_announcement.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             age_groups=age_groups,
                             skill_levels=skill_levels)
    if len(city) > 50:
        flash("VIRHE: Kaupunki on liian pitkä (max 50 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("edit_announcement.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             age_groups=age_groups,
                             skill_levels=skill_levels)
    if len(description) > 1000:
        flash("VIRHE: Kuvaus on liian pitkä (max 1000 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("edit_announcement.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             age_groups=age_groups,
                             skill_levels=skill_levels)

    # Validate that age_group and skill_level are from allowed options
    valid_age_groups = [option["value"] for option in age_groups]
    valid_skill_levels = [option["value"] for option in skill_levels]
    if age_group not in valid_age_groups:
        flash("VIRHE: virheellinen ikäryhmä")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("edit_announcement.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             age_groups=age_groups,
                             skill_levels=skill_levels)
    if skill_level not in valid_skill_levels:
        flash("VIRHE: virheellinen taitotaso")
        filled = {
            "sport": sport,
            "city": city,
            "age_group": age_group,
            "skill_level": skill_level,
            "description": description
        }
        return render_template("edit_announcement.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             age_groups=age_groups,
                             skill_levels=skill_levels)
    announcements_student.update_announcement(
        announcement_id, sport, city, age_group, skill_level, description)
    flash("Oppilasilmoitus päivitetty onnistuneesti")
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
        ensure_csrf_token()
        return render_template("remove_announcement.html", announcement=a)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            announcements_student.remove_announcement(announcement_id)
            flash("Ilmoitus poistettu onnistuneesti")
            return redirect("/")
        return redirect("/announcement/" + str(announcement_id))
    # This should never be reached, but added for completeness
    return redirect("/")

@app.route("/choose_announcement_type")
def choose_announcement_type():
    login_check = require_login()
    if login_check:
        return login_check
    return render_template("choose_announcement_type.html")

@app.route("/create_announcement_coach", methods=["GET", "POST"])
def create_announcement_coach():
    login_check = require_login()
    if login_check:
        return login_check
    if request.method == "GET":
        ensure_csrf_token()
        experience_levels = get_coach_form_options()
        return render_template("create_announcement_coach.html",
                             experience_levels=experience_levels,
                             filled={})
    check_csrf()
    sport = request.form.get("sport", "").strip()
    city = request.form.get("city", "").strip()
    experience_level = request.form.get("experience_level", "").strip()
    description = request.form.get("description", "").strip()

    # Get form options for validation and template rendering
    experience_levels = get_coach_form_options()
    if not sport:
        flash("VIRHE: Laji on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("create_announcement_coach.html",
                             experience_levels=experience_levels,
                             filled=filled)
    if not city:
        flash("VIRHE: Kaupunki on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("create_announcement_coach.html",
                             experience_levels=experience_levels,
                             filled=filled)
    if not experience_level:
        flash("VIRHE: Kokemustaso on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("create_announcement_coach.html",
                             experience_levels=experience_levels,
                             filled=filled)
    if not description:
        flash("VIRHE: Kuvaus on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("create_announcement_coach.html",
                             experience_levels=experience_levels,
                             filled=filled)
    if len(sport) > 50:
        flash("VIRHE: Laji on liian pitkä (max 50 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("create_announcement_coach.html",
                             experience_levels=experience_levels,
                             filled=filled)
    if len(city) > 50:
        flash("VIRHE: Kaupunki on liian pitkä (max 50 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("create_announcement_coach.html",
                             experience_levels=experience_levels,
                             filled=filled)
    if len(description) > 1000:
        flash("VIRHE: Kuvaus on liian pitkä (max 1000 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("create_announcement_coach.html",
                             experience_levels=experience_levels,
                             filled=filled)
    # Validate that experience_level is from allowed options
    valid_experience_levels = [option["value"] for option in experience_levels]
    if experience_level not in valid_experience_levels:
        flash("VIRHE: virheellinen kokemustaso")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("create_announcement_coach.html",
                             experience_levels=experience_levels,
                             filled=filled)
    user_id = session["user_id"]
    announcements_coach.add_announcement(
        sport, city, experience_level, description, user_id)
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
    classes = announcements_coach.get_classes(announcement_id)
    experience_levels = get_coach_form_options()
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

    # Get form options for validation and template rendering
    experience_levels = get_coach_form_options()
    classes = announcements_coach.get_classes(announcement_id)
    if not sport:
        flash("VIRHE: Laji on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("edit_announcement_coach.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             experience_levels=experience_levels)
    if not city:
        flash("VIRHE: Kaupunki on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("edit_announcement_coach.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             experience_levels=experience_levels)
    if not experience_level:
        flash("VIRHE: Kokemustaso on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("edit_announcement_coach.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             experience_levels=experience_levels)
    if not description:
        flash("VIRHE: Kuvaus on pakollinen")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("edit_announcement_coach.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             experience_levels=experience_levels)

    if len(sport) > 50:
        flash("VIRHE: Laji on liian pitkä (max 50 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("edit_announcement_coach.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             experience_levels=experience_levels)
    if len(city) > 50:
        flash("VIRHE: Kaupunki on liian pitkä (max 50 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("edit_announcement_coach.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             experience_levels=experience_levels)
    if len(description) > 1000:
        flash("VIRHE: Kuvaus on liian pitkä (max 1000 merkkiä)")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("edit_announcement_coach.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             experience_levels=experience_levels)

    # Validate that experience_level is from allowed options
    valid_experience_levels = [option["value"] for option in experience_levels]
    if experience_level not in valid_experience_levels:
        flash("VIRHE: virheellinen kokemustaso")
        filled = {
            "sport": sport,
            "city": city,
            "experience_level": experience_level,
            "description": description
        }
        return render_template("edit_announcement_coach.html",
                             announcement={"id": announcement_id, **filled},
                             classes=classes,
                             experience_levels=experience_levels)
    announcements_coach.update_announcement(
        announcement_id, sport, city, experience_level, description)
    flash("Valmentajailmoitus päivitetty onnistuneesti")
    return redirect("/announcement_coach/" + str(announcement_id))

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
            flash("Ilmoitus poistettu onnistuneesti")
            return redirect("/")
        return redirect("/announcement_coach/" + str(announcement_id))
    # This should never be reached, but added for completeness
    return redirect("/")

@app.route("/mark_announcement_coach_found/<int:announcement_id>", methods=["POST"])
def mark_announcement_coach_found(announcement_id):
    login_check = require_login()
    if login_check:
        return login_check
    check_csrf()
    a = announcements_coach.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    if a["user_id"] != session["user_id"]:
        return ui.handle_announcement_forbidden("merkitä")
    announcements_coach.mark_announcement_found(announcement_id)
    flash("Ilmoitus merkitty löydetyksi")
    return redirect("/announcement_coach/" + str(announcement_id))

@app.route("/mark_announcement_coach_not_found/<int:announcement_id>", methods=["POST"])
def mark_announcement_coach_not_found(announcement_id):
    login_check = require_login()
    if login_check:
        return login_check
    check_csrf()
    a = announcements_coach.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    if a["user_id"] != session["user_id"]:
        return ui.handle_announcement_forbidden("merkitä")
    announcements_coach.mark_announcement_not_found(announcement_id)
    flash("Löydetty -merkintä poistettu")
    return redirect("/announcement_coach/" + str(announcement_id))

@app.route("/mark_announcement_found/<int:announcement_id>", methods=["POST"])
def mark_announcement_found(announcement_id):
    login_check = require_login()
    if login_check:
        return login_check
    check_csrf()
    a = announcements_student.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    if a["user_id"] != session["user_id"]:
        return ui.handle_announcement_forbidden("merkitä")
    announcements_student.mark_announcement_found(announcement_id)
    flash("Ilmoitus merkitty löydetyksi")
    return redirect("/announcement/" + str(announcement_id))

@app.route("/mark_announcement_not_found/<int:announcement_id>", methods=["POST"])
def mark_announcement_not_found(announcement_id):
    login_check = require_login()
    if login_check:
        return login_check
    check_csrf()
    a = announcements_student.get_announcement(announcement_id)
    if not a:
        return ui.handle_announcement_not_found()
    if a["user_id"] != session["user_id"]:
        return ui.handle_announcement_forbidden("merkitä")
    announcements_student.mark_announcement_not_found(announcement_id)
    flash("Löydetty -merkintä poistettu")
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
        ensure_csrf_token()
        # Check for recipient query parameter to pre-fill the form
        recipient = request.args.get("recipient", "")
        filled = {"recipient": recipient, "body": ""}
        return render_template("message_new.html", filled=filled)
    check_csrf()
    me = session["user_id"]
    recipient_username = request.form.get("recipient", "").strip()
    body = request.form.get("body", "").strip()
    if not recipient_username or not body:
        flash("VIRHE: vastaanottaja ja viesti ovat pakollisia")
        filled = {"recipient": recipient_username, "body": body}
        return render_template("message_new.html", filled=filled)
    if len(body) > 2000:
        flash("VIRHE: viesti on liian pitkä (max 2000 merkkiä)")
        filled = {"recipient": recipient_username, "body": body}
        return render_template("message_new.html", filled=filled)
    rec = users.find_user_id_by_username(recipient_username)
    if not rec:
        flash("VIRHE: vastaanottajaa ei löydy")
        filled = {"recipient": recipient_username, "body": body}
        return render_template("message_new.html", filled=filled)
    other_id = rec["id"]
    if other_id == me:
        flash("VIRHE: et voi lähettää viestiä itsellesi")
        filled = {"recipient": recipient_username, "body": body}
        return render_template("message_new.html", filled=filled)
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
    return render_template("messages_thread.html",
                         other_user=other_user,
                         messages=msgs,
                         thread_id=thread_id)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

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

    if not rows or not check_password_hash(rows[0]["password_hash"], password):
        flash("VIRHE: väärä tunnus tai salasana")
        filled = {"username": username}
        return render_template("login.html", filled=filled, next_page=next_page)

    # Login successful
    session["user_id"] = rows[0]["id"]
    session["username"] = username
    session["csrf_token"] = secrets.token_hex(16)
    return redirect(next_page)

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
    
    # Calculate age distribution for student announcements
    all_student_announcements = announcements_student.get_announcements()
    age_group_counts = {}
    total_announcements = len(all_student_announcements)
    
    # Count age groups
    for announcement in all_student_announcements:
        age_group = announcement['age_group']
        if age_group:
            age_group_counts[age_group] = age_group_counts.get(age_group, 0) + 1
    
    # Get all possible age groups from classes table to ensure all are shown
    all_age_groups = announcements_student.get_all_classes().get("Ikäryhmä", [])
    
    # Calculate percentages and create distribution data for all age groups
    age_distribution = []
    for age_group in all_age_groups:
        count = age_group_counts.get(age_group, 0)
        percentage = round((count / total_announcements) * 100, 1) if total_announcements > 0 else 0
        age_distribution.append({
            'age_group': age_group,
            'count': count,
            'percentage': percentage
        })
    
    # Sort by percentage (descending)
    age_distribution.sort(key=lambda x: x['percentage'], reverse=True)
    
    # Find user's age group and percentage
    user_age_group = None
    user_percentage = 0
    
    # Get user's student announcements to find their age group
    user_student_announcements = announcements_student.get_announcements_by_user(user_id)
    if user_student_announcements:
        # Find the most common age group for this user
        user_age_groups = [ann['age_group'] for ann in user_student_announcements if ann['age_group']]
        if user_age_groups:
            # Get the most frequent age group for this user
            from collections import Counter
            user_age_group_counts = Counter(user_age_groups)
            user_age_group = user_age_group_counts.most_common(1)[0][0]
            
            # Calculate user's percentage
            user_count = age_group_counts.get(user_age_group, 0)
            user_percentage = round((user_count / total_announcements) * 100, 1) if total_announcements > 0 else 0
    
    ensure_csrf_token()
    return render_template("profile.html",
                         current_display_name=current_display_name,
                         user=user,
                         student_announcements=student_announcements,
                         coach_announcements=coach_announcements,
                         age_distribution=age_distribution,
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
    return render_template("user_profile.html", 
                         user=user, 
                         student_announcements=student_announcements,
                         coach_announcements=coach_announcements)

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    login_check = require_login()
    if login_check:
        return login_check

    if request.method == "GET":
        ensure_csrf_token()
        return render_template("add_image.html")

    if request.method == "POST":
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

@app.route("/confirm_age_group_change", methods=["GET", "POST"])
def confirm_age_group_change():
    login_check = require_login()
    if login_check:
        return login_check
    
    if request.method == "GET":
        ensure_csrf_token()
        # Get pending announcement from session
        pending_announcement = session.get("pending_announcement")
        if not pending_announcement:
            flash("VIRHE: Ei odottavaa ilmoitusta löytynyt")
            return redirect("/create_announcement_student")
        
        return render_template("confirm_age_group_change.html", 
                             pending_announcement=pending_announcement)
    
    check_csrf()
    confirm = request.form.get("confirm")
    
    if confirm == "yes":
        # User confirmed the age group change
        pending_announcement = session.get("pending_announcement")
        if pending_announcement:
            # Update all user's existing announcements to new age group
            user_id = session["user_id"]
            new_age_group = pending_announcement["age_group"]
            
            # Update existing announcements
            sql = "UPDATE announcements_student SET age_group = ? WHERE user_id = ?"
            db.execute(sql, [new_age_group, user_id])
            
            # Update announcement_classes for existing announcements
            sql_classes = "UPDATE announcement_classes SET value = ? WHERE announcement_id IN (SELECT id FROM announcements_student WHERE user_id = ?) AND title = 'Ikäryhmä'"
            db.execute(sql_classes, [new_age_group, user_id])
            
            # Create the new announcement
            announcements_student.add_announcement(
                pending_announcement["sport"],
                pending_announcement["city"],
                pending_announcement["age_group"],
                pending_announcement["skill_level"],
                pending_announcement["description"],
                user_id
            )
            
            # Clear pending announcement from session
            del session["pending_announcement"]
            
            flash("Ikäryhmä päivitetty ja oppilasilmoitus luotu onnistuneesti")
            return redirect("/")
        else:
            flash("VIRHE: Ei odottavaa ilmoitusta löytynyt")
            return redirect("/create_announcement_student")
    
    elif confirm == "no":
        # User declined the age group change, clear pending announcement
        if "pending_announcement" in session:
            del session["pending_announcement"]
        return redirect("/create_announcement_student")
    
    else:
        flash("VIRHE: Virheellinen valinta")
        return redirect("/create_announcement_student")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        if "csrf_token" in session:
            del session["csrf_token"]
    return redirect("/")
