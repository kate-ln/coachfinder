import datetime
import pytz
import db

def _format_finland_time(utc_timestamp_str):
    """Convert UTC timestamp string to Finland timezone (EET/EEST)"""
    if not utc_timestamp_str:
        return ""
    utc_dt = datetime.datetime.fromisoformat(
        utc_timestamp_str.replace(' ', 'T'))
    utc_dt = pytz.UTC.localize(utc_dt)
    finland_tz = pytz.timezone('Europe/Helsinki')
    finland_dt = utc_dt.astimezone(finland_tz)
    return finland_dt.strftime('%Y-%m-%d %H:%M:%S')

def find_existing_thread(user_a_id, user_b_id):
    return db.query("SELECT id FROM threads WHERE user_a_id = ? AND user_b_id = ?", [user_a_id, user_b_id])

def create_thread(user_a_id, user_b_id):
    db.execute("INSERT INTO threads (user_a_id, user_b_id) VALUES (?, ?)", [user_a_id, user_b_id])

def get_user_threads(user_id):
    sql = """
    SELECT
      t.id AS thread_id,
      CASE WHEN t.user_a_id = ? THEN u2.username ELSE u1.username END AS other_username,
      CASE WHEN t.user_a_id = ? THEN u2.display_name ELSE u1.display_name END AS other_display_name,
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
    rows = db.query(sql, [user_id, user_id, user_id, user_id])
    result = []
    for row in rows:
        row_dict = dict(row)
        if row_dict['last_at']:
            row_dict['last_at'] = _format_finland_time(row_dict['last_at'])
        result.append(row_dict)
    return result

def get_thread_participants(thread_id):
    return db.query("SELECT user_a_id, user_b_id FROM threads WHERE id = ?",
                   [thread_id])

def add_message(thread_id, sender_id, body):
    db.execute("INSERT INTO messages (thread_id, sender_id, body) VALUES (?, ?, ?)",
               [thread_id, sender_id, body])

def get_thread_messages(thread_id):
    rows = db.query("""
        SELECT m.id, m.body, m.created_at, u.username AS sender, u.display_name AS sender_display_name
        FROM messages m
        JOIN users u ON u.id = m.sender_id
        WHERE m.thread_id = ?
        ORDER BY m.created_at ASC, m.id ASC
    """, [thread_id])
    result = []
    for row in rows:
        row_dict = dict(row)
        if row_dict['created_at']:
            row_dict['created_at'] = _format_finland_time(row_dict['created_at'])
        result.append(row_dict)
    return result
