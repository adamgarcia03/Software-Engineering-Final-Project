import tkinter as tk

def open_emergency():
    win = tk.Toplevel()
    win.title("Emergency & Quick Access")
    win.geometry("400x260")

    tk.Label(win, text="Emergency Contacts", font=("Arial", 16)).pack(pady=10)

    contacts = [
        "Security: 911 or campus x1234",
        "Counseling: (123) 456-7890",
        "Health Services: (321) 654-0987",
    ]

    for contact in contacts:
        tk.Button(win, text=contact, width=40).pack(pady=5)

#Purpose: Quick access to emergency contacts.

