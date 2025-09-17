CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE announcements_student (
    id INTEGER PRIMARY KEY,
    sport TEXT,
    city TEXT,
    age_group TEXT,
    skill_level TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users
);