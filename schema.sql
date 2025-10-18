CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    display_name TEXT
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

CREATE TABLE threads (
  id INTEGER PRIMARY KEY,
  user_a_id INTEGER REFERENCES users(id),
  user_b_id INTEGER REFERENCES users(id),
  created_at TEXT DEFAULT (datetime('now')),
  UNIQUE(user_a_id, user_b_id)
);

CREATE TABLE messages (
  id INTEGER PRIMARY KEY,
  thread_id INTEGER REFERENCES threads(id) ON DELETE CASCADE,
  sender_id INTEGER REFERENCES users(id),
  body TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE classes (
  id INTEGER PRIMARY KEY,
  title TEXT,
  value TEXT
);

CREATE TABLE announcements_coach (
    id INTEGER PRIMARY KEY,
    sport TEXT,
    city TEXT,
    experience_level TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE  announcement_classes (
  id INTEGER PRIMARY KEY,
  announcement_id INTEGER REFERENCES announcements_student(id),
  title TEXT,
  value TEXT
);

CREATE TABLE announcement_classes_coach (
  id INTEGER PRIMARY KEY,
  announcement_id INTEGER REFERENCES announcements_coach(id),
  title TEXT,
  value TEXT
);