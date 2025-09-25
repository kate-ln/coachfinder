import db

def get_user_profile(user_id):
    return db.query("SELECT display_name FROM users WHERE id = ?", [user_id])

def create_user(username, password_hash):
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", [username, password_hash])

def get_user_by_username(username):
    return db.query("SELECT id, password_hash FROM users WHERE username = ?", [username])

def get_user_by_id(user_id):
    result = db.query("SELECT username, display_name FROM users WHERE id = ?", [user_id])
    return result[0] if result else None

def update_user_display_name(user_id, display_name):
    db.execute("UPDATE users SET display_name = ? WHERE id = ?", [display_name, user_id])

def find_user_id_by_username(username):
    result = db.query("SELECT id FROM users WHERE username = ?", [username])
    return result[0] if result else None