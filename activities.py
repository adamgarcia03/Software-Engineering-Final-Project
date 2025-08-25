import tkinter as tk
from tkinter import messagebox
import sqlite3
from db_setup import get_db_path
from tkcalendar import DateEntry
from datetime import date

DB_PATH = get_db_path()

def get_connection():
    return sqlite3.connect(DB_PATH)

def to_iso(d):
    if isinstance(d, date):
        return d.isoformat()
    try:
        m, d2, y = str(d).split("/")
        return f"{int(y):04d}-{int(m):02d}-{int(d2):02d}"
    except Exception:
        return date.today().isoformat()

def open_activities():
    window = tk.Toplevel()
    window.title("Weekly Activities")
    window.geometry("560x600")

    tk.Label(window, text="Activity").pack()
    entry = tk.Entry(window, width=50)
    entry.pack(pady=4)

    tk.Label(window, text="Club").pack()
    club_var = tk.StringVar(value="Robotics")
    club_menu = tk.OptionMenu(window, club_var, "Robotics", "Civil", "Software", "Electrical")
    club_menu.pack(pady=4)

    tk.Label(window, text="Date").pack()
    date_picker = DateEntry(window, width=16, background="white", foreground="black", borderwidth=1)
    date_picker.pack(pady=4)

    listbox = tk.Listbox(window, width=72, height=16)
    listbox.pack(pady=6)

    list_ids = [] 

    def load_data():
        listbox.delete(0, tk.END)
        list_ids.clear()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, content, club, IFNULL(day, '') as day FROM activities ORDER BY id DESC
        """)
        for row in cur.fetchall():
            aid, content, club, day = row
            prefix_date = f"[{day}] " if day else ""
            listbox.insert(tk.END, f"{club} - {prefix_date}{content}")  
            list_ids.append(aid) 
        conn.close()

    def add():
        text = entry.get().strip()
        club = club_var.get()
        if not text:
            return
        day_iso = to_iso(date_picker.get_date())
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO activities (content, club, day) VALUES (?, ?, ?)", (text, club, day_iso))
        activity_id = cur.lastrowid
        cur.execute("""
            INSERT OR REPLACE INTO events (activity_id, day, description)
            VALUES (?, ?, ?)
        """, (activity_id, day_iso, text))
        conn.commit()
        conn.close()
        load_data()
        entry.delete(0, tk.END)

    def delete():
        try:
            index = listbox.curselection()[0]
            activity_id = list_ids[index]
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM events WHERE activity_id=?", (activity_id,))
            cur.execute("DELETE FROM activities WHERE id=?", (activity_id,))
            conn.commit()
            conn.close()
            load_data()
            entry.delete(0, tk.END)
        except IndexError:
            messagebox.showerror("Error", "No item selected.")

    def edit():
        try:
            index = listbox.curselection()[0]
            activity_id = list_ids[index]
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT content, club, day FROM activities WHERE id=?", (activity_id,))
            row = cur.fetchone()
            conn.close()
            if row:
                content, club, day = row
                entry.delete(0, tk.END)
                entry.insert(0, content)
                club_var.set(club)
                try:
                    y, m, d = map(int, day.split("-"))
                    date_picker.set_date(date(y, m, d))
                except:
                    pass
        except IndexError:
            messagebox.showerror("Error", "No item selected.")

    def update():
        try:
            index = listbox.curselection()[0]
            activity_id = list_ids[index]
            new_text = entry.get().strip()
            new_club = club_var.get()
            new_day = to_iso(date_picker.get_date())
            if not new_text:
                messagebox.showerror("Error", "Activity content cannot be empty.")
                return
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE activities SET content=?, club=?, day=? WHERE id=?",
                        (new_text, new_club, new_day, activity_id))
            cur.execute("""
                INSERT INTO events (activity_id, day, description)
                VALUES (?, ?, ?)
                ON CONFLICT(activity_id) DO UPDATE SET day=excluded.day, description=excluded.description
            """, (activity_id, new_day, new_text))
            conn.commit()
            conn.close()
            load_data()
            entry.delete(0, tk.END)
        except IndexError:
            messagebox.showerror("Error", "Select an item first.")

    tk.Button(window, text="Add Activity", command=add).pack(pady=2)
    tk.Button(window, text="Edit Selected", command=edit).pack(pady=2)
    tk.Button(window, text="Update Edited", command=update).pack(pady=2)
    tk.Button(window, text="Delete Selected", command=delete).pack(pady=2)

    load_data()

#Purpose: Manage weekly activities; store in DB and sync with events table for calendar.

