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

def get_announcement(announcement_id):
    sql = """SELECT announcements_student.sport,
                    announcements_student.city,
                    announcements_student.age_group,
                    announcements_student.skill_level,
                    announcements_student.description,
                    users.username
             FROM announcements_student, users
             WHERE announcements_student.user_id = users.id AND
                   announcements_student.id = ?"""
    return db.query(sql, [announcement_id])[0]