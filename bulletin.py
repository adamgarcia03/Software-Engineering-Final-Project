import tkinter as tk
from tkinter import messagebox
import sqlite3
from db_setup import get_db_path
from tkcalendar import DateEntry
from datetime import date

DB_PATH = get_db_path()

def get_connection():
    return sqlite3.connect(DB_PATH)

def open_bulletin():
    win = tk.Toplevel()
    win.title("Bulletin Board")
    win.geometry("520x520")

    tk.Label(win, text="Date").pack()
    date_picker = DateEntry(win, width=16, background="white", foreground="black", borderwidth=1)
    date_picker.pack(pady=4)

    entry = tk.Entry(win, width=54)
    entry.pack(pady=10)

    board = tk.Listbox(win, width=66, height=16)
    board.pack()

    def load_data():
        board.delete(0, tk.END)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT content, day FROM bulletin ORDER BY day DESC")
        for row in cursor.fetchall():
            content, day = row
            prefix_date = f"[{day}] " if day else ""
            board.insert(tk.END, f"{prefix_date}{content}")  
        conn.close()

    def post():
        text = entry.get().strip()
        if text:
            day_iso = date_picker.get_date().isoformat()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO bulletin (content, day) VALUES (?, ?)", (text, day_iso))
            conn.commit()
            conn.close()
            load_data()
            entry.delete(0, tk.END)

    def delete():
        try:
            selected = board.get(board.curselection())
            text_only = selected.split("] ", 1)[1]
        except Exception:
            messagebox.showerror("Error", "Select a post to delete.")
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bulletin WHERE content=?", (text_only,))
        conn.commit()
        conn.close()
        load_data()
        entry.delete(0, tk.END)

    def edit():
        try:
            selected = board.get(board.curselection())
            text_only = selected.split("] ", 1)[1]
            entry.delete(0, tk.END)
            entry.insert(0, text_only)
        except Exception:
            messagebox.showerror("Error", "Select a post to edit.")

    def update():
        try:
            selected = board.get(board.curselection())
            old_text = selected.split("] ", 1)[1]
        except Exception:
            messagebox.showerror("Error", "Select a post to update.")
            return
        new_text = entry.get().strip()
        new_day = date_picker.get_date().isoformat()
        if not new_text:
            messagebox.showerror("Error", "Content cannot be empty.")
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE bulletin SET content=?, day=? WHERE content=?", (new_text, new_day, old_text))
        conn.commit()
        conn.close()
        load_data()
        entry.delete(0, tk.END)

    tk.Button(win, text="Post", command=post).pack(pady=2)
    tk.Button(win, text="Edit Selected", command=edit).pack(pady=2)
    tk.Button(win, text="Update Edited", command=update).pack(pady=2)
    tk.Button(win, text="Delete", command=delete).pack(pady=2)
    load_data()

#Purpose: Manage announcements; they can now automatically appear in the calendar.