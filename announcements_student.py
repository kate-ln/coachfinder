import db

def add_announcement(sport, city, age_group, skill_level, description, user_id):
    sql = """
        INSERT INTO announcements_student (sport, city, age_group, skill_level, description, user_id) VALUES
        (?, ?, ?, ?, ?, ?)
    """
    db.execute(sql, [sport, city, age_group, skill_level, description, user_id])

def get_announcements():
    sql = "SELECT id, sport, city, age_group, skill_level, description FROM announcements_student ORDER BY id DESC"
    return db.query(sql)