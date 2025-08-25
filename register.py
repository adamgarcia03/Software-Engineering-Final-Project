import tkinter as tk
from tkinter import messagebox
import sqlite3
from db_setup import get_db_path

DB_PATH = get_db_path()

def get_connection():
    return sqlite3.connect(DB_PATH)

def show_register():
    root = tk.Tk()
    root.title("Register")
    root.geometry("400x350")

    tk.Label(root, text="Register Account", font=("Helvetica", 16)).pack(pady=10)

    labels = ["Username", "Password", "Email", "Full Name"]
    entries = {}

    for field in labels:
        tk.Label(root, text=field).pack()
        show_mask = {"Password": "*"}.get(field)
        entry = tk.Entry(root, show=show_mask)
        entry.pack(pady=5)
        entries[field] = entry

    def register():
        username = entries["Username"].get().strip()
        password = entries["Password"].get()
        email = entries["Email"].get().strip()
        full_name = entries["Full Name"].get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password required")
            return

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email, full_name) VALUES (?, ?, ?, ?)",
                (username, password, email, full_name)
            )
            conn.commit()
            messagebox.showinfo("Success", "Registration successful. Please log in.")
            root.destroy()
            import login
            login.show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()

    tk.Button(root, text="Register", command=register).pack(pady=10)
    root.mainloop()


#Purpose: Purpose: Handles new user registration and ensures unique usernames.