#!/usr/bin/env python3
"""
Simple test data generation script for performance testing.
Creates large amounts of data to test application performance.
"""

import random
import sqlite3
import time

def generate_test_data():
    """Generate test data for performance testing"""
    print("Starting test data generation...")

    # Connect to database
    db = sqlite3.connect("database.db")
    db.execute("PRAGMA foreign_keys = ON")

    # Clear existing data (in correct order to respect foreign keys)
    print("Clearing existing data...")
    db.execute("DELETE FROM messages")
    db.execute("DELETE FROM threads")
    db.execute("DELETE FROM announcement_classes")
    db.execute("DELETE FROM announcement_classes_coach")
    db.execute("DELETE FROM announcements_student")
    db.execute("DELETE FROM announcements_coach")
    db.execute("DELETE FROM users")
    db.execute("DELETE FROM classes")

    # Data sizes
    user_count = 1000
    thread_count = 10000  # Reduced to avoid unique constraint issues
    message_count = 100000  # Reduced proportionally

    print(f"Generating {user_count} users...")
    start_time = time.time()

    # Generate users
    for i in range(1, user_count + 1):
        db.execute("INSERT INTO users (username, password_hash, display_name) VALUES (?, ?, ?)",
                   [f"user{i}", "hashed_password", f"User {i}"])

    user_time = time.time() - start_time
    print(f"Users generated in {user_time:.2f} seconds")

    print(f"Generating {thread_count} threads...")
    start_time = time.time()

    # Generate threads with unique pairs
    created_pairs = set()
    for i in range(1, thread_count + 1):
        user_a_id = random.randint(1, user_count)
        user_b_id = random.randint(1, user_count)
        # Ensure different users
        while user_b_id == user_a_id:
            user_b_id = random.randint(1, user_count)

        # Ensure unique pairs
        pair = (min(user_a_id, user_b_id), max(user_a_id, user_b_id))
        attempts = 0
        while pair in created_pairs and attempts < 100:
            user_a_id = random.randint(1, user_count)
            user_b_id = random.randint(1, user_count)
            while user_b_id == user_a_id:
                user_b_id = random.randint(1, user_count)
            pair = (min(user_a_id, user_b_id), max(user_a_id, user_b_id))
            attempts += 1

        if pair not in created_pairs:
            created_pairs.add(pair)
            db.execute("INSERT INTO threads (user_a_id, user_b_id) VALUES (?, ?)",
                       [user_a_id, user_b_id])

    thread_time = time.time() - start_time
    print(f"Threads generated in {thread_time:.2f} seconds")

    print(f"Generating {message_count} messages...")
    start_time = time.time()

    # Generate messages
    for i in range(1, message_count + 1):
        thread_id = random.randint(1, thread_count)
        sender_id = random.randint(1, user_count)
        content = f"Test message {i}"
        db.execute("""INSERT INTO messages (thread_id, sender_id, body, created_at)
                      VALUES (?, ?, ?, datetime('now'))""",
                   [thread_id, sender_id, content])

    message_time = time.time() - start_time
    print(f"Messages generated in {message_time:.2f} seconds")

    # Generate some announcements for testing
    print("Generating announcements...")
    start_time = time.time()

    # Generate student announcements
    for i in range(1, 1000):
        user_id = random.randint(1, user_count)
        sport = random.choice(["Tennis", "Uinti", "Juoksu", "Jalkapallo", "Koripallo"])
        city = random.choice(["Helsinki", "Tampere", "Turku", "Oulu", "Jyväskylä"])
        age_group = random.choice(["10-15 vuotta", "16-20 vuotta", "21-30 vuotta", "31-40 vuotta"])
        skill_level = random.choice(["Aloittelija", "Keskitaso", "Edistynyt"])
        description = f"Test student announcement {i}"
        db.execute("""INSERT INTO announcements_student
                      (sport, city, age_group, skill_level, description, user_id, found)
                      VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   [sport, city, age_group, skill_level, description, user_id, random.randint(0, 1)])

    # Generate coach announcements
    for i in range(1, 1000):
        user_id = random.randint(1, user_count)
        sport = random.choice(["Tennis", "Uinti", "Juoksu", "Jalkapallo", "Koripallo"])
        city = random.choice(["Helsinki", "Tampere", "Turku", "Oulu", "Jyväskylä"])
        experience_level = random.choice(["Aloittelija", "Keskitaso", "Ammattilainen"])
        description = f"Test coach announcement {i}"
        db.execute("""INSERT INTO announcements_coach
                      (sport, city, experience_level, description, user_id, found)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   [sport, city, experience_level, description, user_id, random.randint(0, 1)])

    announcement_time = time.time() - start_time
    print(f"Announcements generated in {announcement_time:.2f} seconds")

    # Commit and close
    db.commit()
    db.close()

    total_time = user_time + thread_time + message_time + announcement_time
    print(f"\nTest data generation completed in {total_time:.2f} seconds")
    print("Generated:")
    print(f"- {user_count} users")
    print(f"- {thread_count} threads")
    print(f"- {message_count} messages")
    print(f"- 1000 student announcements")
    print(f"- 1000 coach announcements")

if __name__ == "__main__":
    generate_test_data()
