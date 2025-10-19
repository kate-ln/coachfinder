import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)
    classes = {}
    for title, value in result:
        if title not in classes:
            classes[title] = []
        classes[title].append(value)

    return classes

def add_announcement(sport, city, age_group, skill_level, description, user_id):
    sql = """
        INSERT INTO announcements_student (sport, city, age_group, skill_level, description, user_id) VALUES
        (?, ?, ?, ?, ?, ?)
    """
    db.execute(sql, [sport, city, age_group, skill_level, description, user_id])
    announcement_id = db.last_insert_id()
    if age_group:
        update_announcement_class(announcement_id, 'Ikäryhmä', age_group)
    if skill_level:
        update_announcement_class(announcement_id, 'Taitotaso', skill_level)

def get_announcements():
    sql = """SELECT announcements_student.id,
                    announcements_student.sport,
                    announcements_student.city,
                    announcements_student.age_group,
                    announcements_student.skill_level,
                    announcements_student.description,
                    announcements_student.found,
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
                    announcements_student.found,
                    users.id user_id,
                    users.username,
                    users.display_name
             FROM announcements_student
             JOIN users ON announcements_student.user_id = users.id
             WHERE announcements_student.id = ?"""
    result = db.query(sql, [announcement_id])
    if result:
        announcement = dict(result[0])
        classes = []
        if announcement['age_group']:
            classes.append({'title': 'Ikäryhmä', 'value': announcement['age_group']})
        if announcement['skill_level']:
            classes.append({'title': 'Taitotaso', 'value': announcement['skill_level']})
        announcement['classes'] = classes
        return announcement
    return None

def get_classes(announcement_id):
    sql = "SELECT title, value FROM announcement_classes WHERE announcement_id = ?"
    return db.query(sql, [announcement_id])

def update_announcement(announcement_id, sport, city, age_group, skill_level, description):
    sql = """UPDATE announcements_student SET sport = ?,
                                              city = ?,
                                              age_group = ?,
                                              skill_level = ?,
                                              description = ?
                                          WHERE id = ?"""
    db.execute(sql, [sport, city, age_group, skill_level, description, announcement_id])
    if age_group:
        update_announcement_class(announcement_id, 'Ikäryhmä', age_group)
    if skill_level:
        update_announcement_class(announcement_id, 'Taitotaso', skill_level)

def remove_announcement(announcement_id):
    # First delete related records in announcement_classes table
    sql_classes = "DELETE FROM announcement_classes WHERE announcement_id = ?"
    db.execute(sql_classes, [announcement_id])
    # Then delete the announcement itself
    sql = "DELETE FROM announcements_student WHERE id = ?"
    db.execute(sql, [announcement_id])

def find_announcements(query, active_only=False):
    sql = """SELECT announcements_student.id,
                    announcements_student.sport,
                    announcements_student.city,
                    announcements_student.age_group,
                    announcements_student.skill_level,
                    announcements_student.found,
                    users.display_name,
                    users.username
             FROM announcements_student
             JOIN users ON announcements_student.user_id = users.id
             WHERE (sport LIKE ? OR city LIKE ? OR age_group LIKE ? OR skill_level LIKE ? OR description LIKE ?)"""

    if active_only:
        sql += " AND announcements_student.found = 0"

    sql += " ORDER BY announcements_student.id DESC"

    l = "%" + query + "%"
    return db.query(sql, [l, l, l, l, l])

def get_announcements_by_user(user_id):
    sql = """SELECT announcements_student.id,
                    announcements_student.sport,
                    announcements_student.city,
                    announcements_student.age_group,
                    announcements_student.skill_level,
                    announcements_student.description,
                    announcements_student.found,
                    users.username,
                    users.display_name
             FROM announcements_student
             JOIN users ON announcements_student.user_id = users.id
             WHERE announcements_student.user_id = ?
             ORDER BY announcements_student.id DESC"""
    return db.query(sql, [user_id])

def mark_announcement_found(announcement_id):
    """Mark an announcement as found (Valmentaja löydetty)"""
    sql = "UPDATE announcements_student SET found = 1 WHERE id = ?"
    db.execute(sql, [announcement_id])

def mark_announcement_not_found(announcement_id):
    """Mark an announcement as not found (remove Valmentaja löydetty status)"""
    sql = "UPDATE announcements_student SET found = 0 WHERE id = ?"
    db.execute(sql, [announcement_id])

def get_found_announcements():
    """Get all found student announcements"""
    sql = """SELECT announcements_student.id,
                    announcements_student.sport,
                    announcements_student.city,
                    announcements_student.age_group,
                    announcements_student.skill_level,
                    announcements_student.found,
                    users.display_name,
                    users.username
             FROM announcements_student
             JOIN users ON announcements_student.user_id = users.id
             WHERE announcements_student.found = 1
             ORDER BY announcements_student.id DESC"""
    return db.query(sql)

def update_announcement_class(announcement_id, title, value):
    sql_check = "SELECT id FROM announcement_classes WHERE announcement_id = ? AND title = ?"
    existing = db.query(sql_check, [announcement_id, title])
    if existing:
        sql_update = """UPDATE announcement_classes 
                         SET value = ? 
                         WHERE announcement_id = ? AND title = ?"""
        db.execute(sql_update, [value, announcement_id, title])
    else:
        sql_insert = """INSERT INTO announcement_classes 
                        (announcement_id, title, value) VALUES (?, ?, ?)"""
        db.execute(sql_insert, [announcement_id, title, value])
