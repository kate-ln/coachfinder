import db

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
    return db.query(sql, [user_id, user_id, user_id, user_id])

def get_thread_participants(thread_id):
    return db.query("SELECT user_a_id, user_b_id FROM threads WHERE id = ?", [thread_id])

def add_message(thread_id, sender_id, body):
    db.execute("INSERT INTO messages (thread_id, sender_id, body) VALUES (?, ?, ?)", [thread_id, sender_id, body])

def get_thread_messages(thread_id):
    return db.query("""
        SELECT m.id, m.body, m.created_at, u.username AS sender, u.display_name AS sender_display_name
        FROM messages m
        JOIN users u ON u.id = m.sender_id
        WHERE m.thread_id = ?
        ORDER BY m.created_at ASC, m.id ASC
    """, [thread_id])