#!/usr/bin/env python3
"""
Add database indexes to improve performance.
"""

import sqlite3

def add_indexes():
    """Add performance indexes to the database"""
    print("Adding database indexes...")

    db = sqlite3.connect("database.db")

    # Add index for messages.thread_id (most important for performance)
    print("Adding index on messages.thread_id...")
    db.execute("CREATE INDEX IF NOT EXISTS idx_messages_thread_id ON messages (thread_id)")

    # Add index for messages.sender_id
    print("Adding index on messages.sender_id...")
    db.execute("CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages (sender_id)")

    # Add index for threads.user_a_id
    print("Adding index on threads.user_a_id...")
    db.execute("CREATE INDEX IF NOT EXISTS idx_threads_user_a_id ON threads (user_a_id)")

    # Add index for threads.user_b_id
    print("Adding index on threads.user_b_id...")
    db.execute("CREATE INDEX IF NOT EXISTS idx_threads_user_b_id ON threads (user_b_id)")

    # Add index for announcements_student.user_id
    print("Adding index on announcements_student.user_id...")
    db.execute("""CREATE INDEX IF NOT EXISTS idx_announcements_student_user_id
                   ON announcements_student (user_id)""")

    # Add index for announcements_coach.user_id
    print("Adding index on announcements_coach.user_id...")
    db.execute("""CREATE INDEX IF NOT EXISTS idx_announcements_coach_user_id
                   ON announcements_coach (user_id)""")

    # Add index for announcements_student.found
    print("Adding index on announcements_student.found...")
    db.execute("""CREATE INDEX IF NOT EXISTS idx_announcements_student_found
                   ON announcements_student (found)""")

    # Add index for announcements_coach.found
    print("Adding index on announcements_coach.found...")
    db.execute("""CREATE INDEX IF NOT EXISTS idx_announcements_coach_found
                   ON announcements_coach (found)""")

    db.commit()
    db.close()

    print("Database indexes added successfully!")

if __name__ == "__main__":
    add_indexes()
