import sqlite3
import os

DB_DIR = "db"
DB_PATH = os.path.join(DB_DIR, "app.db")

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            full_name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            club TEXT DEFAULT 'General'
        )
    """)
    cursor.execute("PRAGMA table_info(activities)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'day' not in columns:
        cursor.execute("ALTER TABLE activities ADD COLUMN day TEXT DEFAULT ''")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER UNIQUE NOT NULL,
            day TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY(activity_id) REFERENCES activities(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bulletin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    cursor.execute("PRAGMA table_info(bulletin)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'day' not in columns:
        cursor.execute("ALTER TABLE bulletin ADD COLUMN day TEXT DEFAULT ''")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            club TEXT NOT NULL,
            UNIQUE(username, club)
        )
    """)

    conn.commit()
    conn.close()

def get_db_path():
    return DB_PATH

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")

#Purpose: Handles database creation and setup.

