import tkinter as tk
import sqlite3
from tkcalendar import Calendar
from datetime import date, datetime
from db_setup import get_db_path

DB_PATH = get_db_path()

def get_user_subscriptions(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT club FROM subscriptions WHERE username = ?", (username,))
    clubs = [row[0] for row in cursor.fetchall()]
    conn.close()
    return clubs

def update_subscription(username, club, is_checked):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if is_checked:
        cursor.execute("INSERT OR IGNORE INTO subscriptions (username, club) VALUES (?, ?)", (username, club))
    else:
        cursor.execute("DELETE FROM subscriptions WHERE username = ? AND club = ?", (username, club))
    conn.commit()
    conn.close()

def all_events_for_user(username):
    clubs = get_user_subscriptions(username)
    if not clubs:
        return []
    placeholders = ",".join(["?"] * len(clubs))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"""
        SELECT e.day, e.description
        FROM events e
        JOIN activities a ON e.activity_id = a.id
        WHERE a.club IN ({placeholders})
        ORDER BY e.day
    """
    cursor.execute(query, clubs)
    events = cursor.fetchall()
    conn.close()
    return events

def events_on_for_user(username, day_iso):
    clubs = get_user_subscriptions(username)
    if not clubs:
        return []
    placeholders = ",".join(["?"] * len(clubs))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"""
        SELECT e.description
        FROM events e
        JOIN activities a ON e.activity_id = a.id
        WHERE e.day = ? AND a.club IN ({placeholders})
    """
    cursor.execute(query, [day_iso] + clubs)
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def mmddyyyy_to_iso(s):
    try:
        m, d, y = s.split("/")
        return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
    except Exception:
        try:
            datetime.fromisoformat(s)
            return s
        except Exception:
            return date.today().isoformat()

def open_calendar(username):
    win = tk.Toplevel()
    win.title("Event Calendar")
    win.geometry("680x560")

    tk.Label(win, text="Engineering Event Calendar", font=("Arial", 16)).pack(pady=8)

    today = date.today()
    cal = Calendar(
        win,
        selectmode="day",
        year=today.year,
        month=today.month,
        day=today.day,
        date_pattern="mm/dd/yyyy"
    )
    cal.pack(pady=10)

    events_box = tk.Listbox(win, width=80, height=10)
    events_box.pack(pady=6)

    tk.Label(win, text="Subscribe to clubs:").pack(pady=(8, 2))
    subscriptions = get_user_subscriptions(username)
    club_vars = {}

    def on_check(club):
        def inner():
            update_subscription(username, club, club_vars[club].get())
            mark_events_on_calendar()
            load_events_for_selected_date()
        return inner

    for club in ["Robotics", "Civil", "Software", "Electrical"]:
        club_vars[club] = tk.BooleanVar(value=(club in subscriptions))
        cb = tk.Checkbutton(win, text=club, variable=club_vars[club], command=on_check(club))
        cb.pack(anchor="w")

    def mark_events_on_calendar():
        cal.calevent_remove('all')
        for day_iso, _desc in all_events_for_user(username):
            try:
                y, m, d = map(int, day_iso.split("-"))
                cal.calevent_create(date(y, m, d), "Event", "activity")
            except Exception:
                pass
        cal.tag_config('activity')

    def load_events_for_selected_date():
        events_box.delete(0, tk.END)
        selected_iso = mmddyyyy_to_iso(cal.get_date())
        for desc in events_on_for_user(username, selected_iso):
            events_box.insert(tk.END, desc)

    cal.bind("<<CalendarSelected>>", lambda e: load_events_for_selected_date())

    mark_events_on_calendar()
    load_events_for_selected_date()
