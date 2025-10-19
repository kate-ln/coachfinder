#!/usr/bin/env python3
"""
Remove database indexes to test performance without them.
"""

import sqlite3

def remove_indexes():
    """Remove performance indexes from the database"""
    print("Removing database indexes...")
    
    db = sqlite3.connect("database.db")
    
    # Remove all indexes
    indexes_to_remove = [
        "idx_messages_thread_id",
        "idx_messages_sender_id", 
        "idx_threads_user_a_id",
        "idx_threads_user_b_id",
        "idx_announcements_student_user_id",
        "idx_announcements_coach_user_id",
        "idx_announcements_student_found",
        "idx_announcements_coach_found"
    ]
    
    for index_name in indexes_to_remove:
        try:
            print(f"Removing index {index_name}...")
            db.execute(f"DROP INDEX IF EXISTS {index_name}")
        except sqlite3.OperationalError as e:
            print(f"  Could not remove {index_name}: {e}")
    
    db.commit()
    db.close()
    
    print("Database indexes removed!")

if __name__ == "__main__":
    remove_indexes()
