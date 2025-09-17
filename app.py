# Käyttäjä pystyy rekisteröimään sovellukseen tunnuksen ja salasanan, jotka tallennetaan tietokantaan:
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

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

    sql = """
        INSERT INTO announcements_student (sport, city, age_group, skill_level, description, user_id) VALUES
        (?, ?, ?, ?, ?, ?)
    """
    db.execute(sql, [sport, city, age_group, skill_level, description, user_id])
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    # POST
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    # Look up the user; db.query should return a list/iterable of rows
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    rows = db.query(sql, [username])

    # If no user found, behave the same as a bad password (don’t reveal which)
    if not rows:
        return "VIRHE: väärä tunnus tai salasana"

    row = rows[0]
    user_id = row["id"]
    password_hash = row["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")