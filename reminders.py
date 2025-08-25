import tkinter as tk
import sqlite3
from datetime import date
from db_setup import get_db_path

DB_PATH = get_db_path()

def get_connection():
    return sqlite3.connect(DB_PATH)

def open_reminders():
    win = tk.Toplevel()
    win.title("Reminders")
    win.geometry("600x500")

    listbox = tk.Listbox(win, width=80, height=25)
    listbox.pack(pady=10)

    def load_reminders():
        listbox.delete(0, tk.END)
        today_iso = date.today().isoformat()
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT content, day FROM activities WHERE day >= ? ORDER BY day ASC
        """, (today_iso,))
        for content, day in cursor.fetchall():
            listbox.insert(tk.END, f"[Activity] {day} - {content}")

        cursor.execute("""
            SELECT content, day FROM bulletin WHERE day >= ? ORDER BY day ASC
        """, (today_iso,))
        for content, day in cursor.fetchall():
            listbox.insert(tk.END, f"[Announcement] {day} - {content}")

        cursor.execute("DELETE FROM activities WHERE day < ?", (today_iso,))
        cursor.execute("DELETE FROM bulletin WHERE day < ?", (today_iso,))
        conn.commit()
        conn.close()

    tk.Button(win, text="Refresh", command=load_reminders).pack(pady=5)
    load_reminders()

#Purpose: Shows upcoming activities and announcements, cleans old ones.