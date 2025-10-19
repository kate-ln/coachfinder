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

def get_age_distribution():
    """Get age distribution statistics for all users"""
    # Define the fixed order of age groups
    age_groups_order = [
        'lapset (7-12)',
        'nuoret (13-17)', 
        'aikuiset (18-)'
    ]
    
    # Get actual counts from database
    sql = """
        SELECT age_group, COUNT(*) as count
        FROM announcements_student 
        WHERE age_group IS NOT NULL AND age_group != ''
        GROUP BY age_group
    """
    db_results = db.query(sql)
    
    # Create a dictionary of actual counts
    actual_counts = {row['age_group']: row['count'] for row in db_results}
    
    # Create results in fixed order, with 0 count for missing groups
    results = []
    for age_group in age_groups_order:
        count = actual_counts.get(age_group, 0)
        results.append({'age_group': age_group, 'count': count})
    
    return results

def get_user_age_group(user_id):
    """Get the most common age group for a specific user"""
    sql = """
        SELECT age_group, COUNT(*) as count
        FROM announcements_student 
        WHERE user_id = ? AND age_group IS NOT NULL AND age_group != ''
        GROUP BY age_group
        ORDER BY count DESC
        LIMIT 1
    """
    result = db.query(sql, [user_id])
    return result[0]['age_group'] if result else None

def update_announcement_class(announcement_id, title, value):
    sql_check = "SELECT id FROM announcement_classes WHERE announcement_id = ? AND title = ?"
    existing = db.query(sql_check, [announcement_id, title])
    if existing:
        sql_update = ("UPDATE announcement_classes SET value = ? "
                      "WHERE announcement_id = ? AND title = ?")
        db.execute(sql_update, [value, announcement_id, title])
    else:
        sql_insert = ("INSERT INTO announcement_classes (announcement_id, title, value) "
                      "VALUES (?, ?, ?)")
        db.execute(sql_insert, [announcement_id, title, value])

def check_age_group_conflict(user_id, new_age_group):
    sql = """
        SELECT DISTINCT age_group 
        FROM announcements_student 
        WHERE user_id = ? AND age_group IS NOT NULL AND age_group != '' AND age_group != ?
    """
    result = db.query(sql, [user_id, new_age_group])
    return len(result) > 0

def check_age_group_conflict_excluding(user_id, new_age_group, exclude_announcement_id):
    sql = """
        SELECT DISTINCT age_group 
        FROM announcements_student 
        WHERE user_id = ? AND age_group IS NOT NULL AND age_group != '' AND age_group != ? AND id != ?
    """
    result = db.query(sql, [user_id, new_age_group, exclude_announcement_id])
    return len(result) > 0

def update_all_user_age_groups(user_id, new_age_group):
    sql = "UPDATE announcements_student SET age_group = ? WHERE user_id = ?"
    db.execute(sql, [new_age_group, user_id])
    
    sql_classes = "UPDATE announcement_classes SET value = ? WHERE announcement_id IN (SELECT id FROM announcements_student WHERE user_id = ?) AND title = 'Ikäryhmä'"
    db.execute(sql_classes, [new_age_group, user_id])

def mark_announcement_found(announcement_id):
    """Mark an announcement as found (Valmentaja löydetty)"""
    sql = "UPDATE announcements_student SET found = 1 WHERE id = ?"
    db.execute(sql, [announcement_id])

def mark_announcement_not_found(announcement_id):
    """Mark an announcement as not found (remove Valmentaja löydetty status)"""
    sql = "UPDATE announcements_student SET found = 0 WHERE id = ?"
    db.execute(sql, [announcement_id])

def get_found_announcements():
    """Get all found announcements"""
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
             WHERE announcements_student.found = 1
             ORDER BY announcements_student.id DESC"""
    return db.query(sql)
