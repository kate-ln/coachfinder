#!/usr/bin/env python3
"""
Seed script for initial development data.
Creates a small, realistic dataset for development and testing.
"""

import sqlite3

def seed_database():
    """Seed the database with initial development data"""
    print("Seeding database with initial development data...")

    db = sqlite3.connect("database.db")
    db.execute("PRAGMA foreign_keys = ON")

    # Clear existing data
    print("Clearing existing data...")
    db.execute("DELETE FROM messages")
    db.execute("DELETE FROM threads")
    db.execute("DELETE FROM announcement_classes")
    db.execute("DELETE FROM announcement_classes_coach")
    db.execute("DELETE FROM announcements_student")
    db.execute("DELETE FROM announcements_coach")
    db.execute("DELETE FROM users")
    db.execute("DELETE FROM classes")

    # Reset auto-increment counters
    try:
        db.execute("DELETE FROM sqlite_sequence")
    except sqlite3.OperationalError:
        pass

    # Create classes data
    print("Creating classes...")
    classes_data = [
        ("Ikäryhmä", "lapset (7-12)"),
        ("Ikäryhmä", "nuoret (13-17)"),
        ("Ikäryhmä", "aikuiset (18-)"),
        ("Taitotaso", "Aloittelija"),
        ("Taitotaso", "Keskitaso"),
        ("Taitotaso", "Edistynyt"),
        ("Kokemus", "Aloittelija"),
        ("Kokemus", "Keskitaso"),
        ("Kokemus", "Ammattilainen"),
        ("Laji", "Tennis"),
        ("Laji", "Uinti"),
        ("Laji", "Juoksu"),
        ("Laji", "Jalkapallo"),
        ("Laji", "Koripallo"),
        ("Paikkakunta", "Helsinki"),
        ("Paikkakunta", "Tampere"),
        ("Paikkakunta", "Turku"),
        ("Paikkakunta", "Oulu"),
        ("Paikkakunta", "Jyväskylä")
    ]

    for title, value in classes_data:
        db.execute("INSERT INTO classes (title, value) VALUES (?, ?)", [title, value])

    # Create sample users
    print("Creating sample users...")
    users_data = [
        ("alex", "hashed_password", "Alex Virtanen"),
        ("maria", "hashed_password", "Maria Korhonen"),
        ("james", "hashed_password", "James Smith"),
        ("anna", "hashed_password", "Anna Nieminen"),
        ("mika", "hashed_password", "Mika Koskinen"),
        ("sara", "hashed_password", "Sara Lehtonen"),
        ("coach1", "hashed_password", "Coach Matti"),
        ("coach2", "hashed_password", "Coach Liisa"),
        ("coach3", "hashed_password", "Coach Pekka"),
        ("coach4", "hashed_password", "Coach Sanna")
    ]

    for username, password_hash, display_name in users_data:
        db.execute("INSERT INTO users (username, password_hash, display_name) VALUES (?, ?, ?)",
                   [username, password_hash, display_name])

    # Create sample student announcements
    print("Creating sample student announcements...")
    student_announcements = [
        ("Tennis", "Helsinki", "nuoret (13-17)", "Keskitaso", "Etsin tenniksen valmentajaa nuorille. Haluaisin parantaa tekniikkaani ja pelata kilpailuja.", 1, 0),
        ("Uinti", "Tampere", "lapset (7-12)", "Aloittelija", "7-vuotias tyttö etsii uinnin valmentajaa. Haluaisi oppia perusasiat.", 2, 0),
        ("Juoksu", "Turku", "aikuiset (18-)", "Edistynyt", "Etsin juoksun valmentajaa maratonharjoitteluun. Tavoitteena alle 3h maraton.", 3, 0),
        ("Jalkapallo", "Oulu", "nuoret (13-17)", "Keskitaso", "Nuori jalkapalloilija etsii valmentajaa. Haluaisi kehittää peliä ja liikkeitä.", 4, 0),
        ("Koripallo", "Jyväskylä", "nuoret (13-17)", "Aloittelija", "Aloittelija etsii koripallon valmentajaa. Haluaisi oppia perusasiat.", 5, 0)
    ]

    for sport, city, age_group, skill_level, description, user_id, found in student_announcements:
        db.execute("""INSERT INTO announcements_student
                      (sport, city, age_group, skill_level, description, user_id, found)
                      VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   [sport, city, age_group, skill_level, description, user_id, found])

    # Create sample coach announcements
    print("Creating sample coach announcements...")
    coach_announcements = [
        ("Tennis", "Helsinki", "Ammattilainen", "Kokenein tenniksen valmentaja etsii uusia oppilaita. Erityisosaamista nuorten valmennuksessa.", 6, 0),
        ("Uinti", "Tampere", "Keskitaso", "Uinnin valmentaja etsii lapsia oppilaisiksi. Kymmenen vuoden kokemus lasten uinnista.", 7, 0),
        ("Juoksu", "Turku", "Ammattilainen", "Maratonvalmentaja etsii kunnianhimoisia juoksijoita. Autan saavuttamaan henkilökohtaiset tavoitteet.", 8, 0),
        ("Jalkapallo", "Oulu", "Keskitaso", "Jalkapallon valmentaja etsii nuoria pelaajia. Fokus tekniikan ja taktiikan kehittämisessä.", 9, 0),
        ("Koripallo", "Jyväskylä", "Aloittelija", "Koripallon valmentaja aloittelijoille. Autan oppimaan perusasiat ja rakentamaan vahvan pohjan.", 10, 0)
    ]

    for sport, city, experience_level, description, user_id, found in coach_announcements:
        db.execute("""INSERT INTO announcements_coach
                      (sport, city, experience_level, description, user_id, found)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   [sport, city, experience_level, description, user_id, found])

    # Create some message threads and messages
    print("Creating sample message threads...")
    threads_data = [
        (1, 6),  # Alex (student) <-> Coach Matti
        (2, 7),  # Maria (student) <-> Coach Liisa
        (3, 8),  # James (student) <-> Coach Pekka
        (4, 9),  # Anna (student) <-> Coach Sanna
        (1, 2),  # Alex <-> Maria (students)
        (6, 7)   # Coach Matti <-> Coach Liisa
    ]

    for user_a_id, user_b_id in threads_data:
        db.execute("INSERT INTO threads (user_a_id, user_b_id) VALUES (?, ?)", [user_a_id, user_b_id])

    # Create sample messages
    print("Creating sample messages...")
    messages_data = [
        (1, 1, "Hei! Olen kiinnostunut tenniksen valmennuksesta. Voitko kertoa lisää?"),
        (1, 6, "Tervetuloa! Olen valmentanut nuoria tenniksen parissa 15 vuotta. Milloin voisimme tavata?"),
        (1, 1, "Loistavaa! Sopiiko ensi viikolla?"),
        (2, 2, "Hei Maria! Haluaisin kysyä uinnin valmennuksesta."),
        (2, 7, "Hei! Kyllä, voin auttaa uinnin perusteissa. Millä tasolla olet tällä hetkellä?"),
        (3, 3, "Hei James! Kuulin että etsit maratonvalmentajaa."),
        (3, 8, "Kyllä! Olen valmentanut useita maratonjuoksijoita. Mikä on tavoitteesi?"),
        (4, 4, "Hei Anna! Jalkapalloharjoitukset kuulostavat mielenkiintoisilta."),
        (4, 9, "Tervetuloa! Harjoittelemme tekniikkaa ja taktiikkaa. Milloin sopii?"),
        (5, 5, "Hei Mika! Koripalloharjoitukset alkavat ensi viikolla.")
    ]

    for thread_id, sender_id, body in messages_data:
        db.execute("""INSERT INTO messages (thread_id, sender_id, body, created_at)
                      VALUES (?, ?, ?, datetime('now'))""",
                   [thread_id, sender_id, body])

    db.commit()
    db.close()

    print("\nDatabase seeded successfully!")
    print("Created:")
    print("- 10 users (5 students, 5 coaches)")
    print("- 5 student announcements")
    print("- 5 coach announcements")
    print("- 6 message threads")
    print("- 10 sample messages")
    print("- 19 class options")
    print("\nYou can now test the application with realistic data!")

if __name__ == "__main__":
    seed_database()
