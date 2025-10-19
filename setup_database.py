#!/usr/bin/env python3
"""
Database setup script for new installations.
This script creates the database schema and populates it with initial data.
"""

import os
import db
from app import app

def setup_database():
    """Set up the database with schema and initial data"""
    print("Setting up database...")

    # Check if database already exists
    if os.path.exists("database.db"):
        print("Database already exists. Skipping schema creation.")
    else:
        print("Creating database schema...")
        # Create database from schema
        os.system("sqlite3 database.db < schema.sql")
        print("Database schema created.")

    with app.app_context():
        # Check if classes data already exists
        result = db.query("SELECT COUNT(*) as count FROM classes")
        if result and result[0]['count'] > 0:
            print("Classes data already exists. Skipping initialization.")
            return

        print("Populating classes data...")

        # Insert age groups
        age_groups = [
            ('Ikäryhmä', 'lapset (7-12)'),
            ('Ikäryhmä', 'nuoret (13-17)'),
            ('Ikäryhmä', 'aikuiset (18-)')
        ]

        # Insert skill levels
        skill_levels = [
            ('Taitotaso', 'aloittelija'),
            ('Taitotaso', 'keskitaso'),
            ('Taitotaso', 'edistynyt'),
            ('Taitotaso', 'kilpataso')
        ]

        # Insert experience levels
        experience_levels = [
            ('Kokemus', 'Alle 3 vuotta'),
            ('Kokemus', '3-6 vuotta'),
            ('Kokemus', 'Yli 6 vuotta')
        ]

        # Insert all data
        all_classes = age_groups + skill_levels + experience_levels

        for title, value in all_classes:
            db.execute("INSERT INTO classes (title, value) VALUES (?, ?)", [title, value])

        print("Database setup completed successfully!")
        print("Classes data populated with:")
        print("- Age groups (Ikäryhmä): lapset (7-12), nuoret (13-17), aikuiset (18-)")
        print("- Skill levels (Taitotaso): aloittelija, keskitaso, edistynyt, kilpataso")
        print("- Experience levels (Kokemus): Alle 3 vuotta, 3-6 vuotta, Yli 6 vuotta")

if __name__ == "__main__":
    setup_database()
