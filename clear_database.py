#!/usr/bin/env python3
"""
Clear all data from the database while preserving the schema.
"""

import sqlite3

def clear_database():
    """Clear all data from the database"""
    print("Clearing database...")

    db = sqlite3.connect("database.db")
    db.execute("PRAGMA foreign_keys = ON")

    # Clear all data in correct order to respect foreign keys
    print("Deleting messages...")
    db.execute("DELETE FROM messages")

    print("Deleting threads...")
    db.execute("DELETE FROM threads")

    print("Deleting announcement classes...")
    db.execute("DELETE FROM announcement_classes")
    db.execute("DELETE FROM announcement_classes_coach")

    print("Deleting announcements...")
    db.execute("DELETE FROM announcements_student")
    db.execute("DELETE FROM announcements_coach")

    print("Deleting users...")
    db.execute("DELETE FROM users")

    print("Deleting classes...")
    db.execute("DELETE FROM classes")

    # Reset auto-increment counters (if table exists)
    print("Resetting auto-increment counters...")
    try:
        db.execute("DELETE FROM sqlite_sequence")
    except sqlite3.OperationalError:
        print("  No sqlite_sequence table found (no auto-increment tables)")

    db.commit()
    db.close()

    print("Database cleared successfully!")
    print("The database schema is preserved and ready for fresh data.")

if __name__ == "__main__":
    clear_database()
