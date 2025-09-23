import db

def add_announcement(sport, city, age_group, skill_level, description, user_id):
    sql = """
        INSERT INTO announcements_student (sport, city, age_group, skill_level, description, user_id) VALUES
        (?, ?, ?, ?, ?, ?)
    """
    db.execute(sql, [sport, city, age_group, skill_level, description, user_id])

def get_announcements():
    sql = """SELECT announcements_student.id,
                    announcements_student.sport,
                    announcements_student.city,
                    announcements_student.age_group,
                    announcements_student.skill_level,
                    announcements_student.description,
                    users.display_name,
                    users.username
             FROM announcements_student
             JOIN users ON announcements_student.user_id = users.id
             ORDER BY announcements_student.id DESC"""
    return db.query(sql)

def get_announcement(announcement_id):
    sql = """SELECT announcements_student.id,
                    announcements_student.sport,
                    announcements_student.city,
                    announcements_student.age_group,
                    announcements_student.skill_level,
                    announcements_student.description,
                    users.id user_id,
                    users.username,
                    users.display_name
             FROM announcements_student
             JOIN users ON announcements_student.user_id = users.id
             WHERE announcements_student.id = ?"""
    result = db.query(sql, [announcement_id])
    return result[0] if result else None

def update_announcement(announcement_id, sport, city, age_group, skill_level, description):
    sql = """UPDATE announcements_student SET sport = ?,
                                              city = ?,
                                              age_group = ?,
                                              skill_level = ?,
                                              description = ?
                                          WHERE id = ?"""
    db.execute(sql, [sport, city, age_group, skill_level, description, announcement_id])

def remove_announcement(announcement_id):
    sql = "DELETE FROM announcements_student WHERE id = ?"
    db.execute(sql, [announcement_id])

def find_announcements(query):
    sql = """SELECT announcements_student.id,
                    announcements_student.sport,
                    users.display_name,
                    users.username
             FROM announcements_student
             JOIN users ON announcements_student.user_id = users.id
             WHERE sport LIKE ? OR city LIKE ? OR age_group LIKE ? OR skill_level LIKE ? OR description LIKE ?
             ORDER BY announcements_student.id DESC"""
    l = "%" + query + "%"
    return db.query(sql, [l, l, l, l, l])