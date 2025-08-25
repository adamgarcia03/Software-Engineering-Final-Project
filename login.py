import tkinter as tk
from tkinter import messagebox
import sqlite3
from db_setup import get_db_path

DB_PATH = get_db_path()

def get_connection():
    return sqlite3.connect(DB_PATH)

def show_login():
    root = tk.Tk()
    root.title("Engineer Social App - Login")
    root.geometry("400x300")

    tk.Label(root, text="Login", font=("Helvetica", 16)).pack(pady=10)

    username_frame = tk.Frame(root)
    username_frame.pack(pady=5)
    tk.Label(username_frame, text="Username:", width=10, anchor="e").pack(side=tk.LEFT)
    username_entry = tk.Entry(username_frame)
    username_entry.pack(side=tk.LEFT)

    password_frame = tk.Frame(root)
    password_frame.pack(pady=5)
    tk.Label(password_frame, text="Password:", width=10, anchor="e").pack(side=tk.LEFT)
    password_entry = tk.Entry(password_frame, show="*")
    password_entry.pack(side=tk.LEFT)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", f"Welcome {username}!")
            root.destroy()
            from dashboard import show_dashboard
            show_dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def go_register():
        root.destroy()
        import register
        register.show_register()

    tk.Button(root, text="Login", command=login).pack(pady=10)
    tk.Button(root, text="Register", command=go_register).pack()

    root.mainloop()


#Purpose: Handles user login; verifies credentials and opens the dashboard.

