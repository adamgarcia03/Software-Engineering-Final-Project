import sqlite3

def init_db():
    conn = sqlite3.connect("engineer_app.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            task TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS bulletins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def get_activities():
    conn = sqlite3.connect("engineer_app.db")
    c = conn.cursor()
    c.execute("SELECT * FROM activities")
    items = c.fetchall()
    conn.close()
    return items

def add_activity(day, task):
    conn = sqlite3.connect("engineer_app.db")
    c = conn.cursor()
    c.execute("INSERT INTO activities (day, task) VALUES (?, ?)", (day, task))
    conn.commit()
    conn.close()

def update_activity(id, task):
    conn = sqlite3.connect("engineer_app.db")
    c = conn.cursor()
    c.execute("UPDATE activities SET task = ? WHERE id = ?", (task, id))
    conn.commit()
    conn.close()

def delete_activity(id):
    conn = sqlite3.connect("engineer_app.db")
    c = conn.cursor()
    c.execute("DELETE FROM activities WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def get_bulletins():
    conn = sqlite3.connect("engineer_app.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bulletins")
    posts = c.fetchall()
    conn.close()
    return posts

def add_bulletin(title, content):
    conn = sqlite3.connect("engineer_app.db")
    c = conn.cursor()
    c.execute("INSERT INTO bulletins (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

def update_bulletin(id, title, content):
    conn = sqlite3.connect("engineer_app.db")
    c = conn.cursor()
    c.execute("UPDATE bulletins SET title = ?, content = ? WHERE id = ?", (title, content, id))
    conn.commit()
    conn.close()

def delete_bulletin(id):
    conn = sqlite3.connect("engineer_app.db")
    c = conn.cursor()
    c.execute("DELETE FROM bulletins WHERE id = ?", (id,))
    conn.commit()
    conn.close()

#Purpose: Older database access functions