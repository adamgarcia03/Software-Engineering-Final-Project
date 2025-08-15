import tkinter as tk

def show_dashboard(username):
    root = tk.Tk()
    root.title("Engineer Social Dashboard")
    root.geometry("600x500")

    tk.Label(root, text=f"Welcome, {username}", font=("Helvetica", 18)).pack(pady=6)
    tk.Label(root, text="Engineer Social", font=("Helvetica", 14)).pack(pady=6)

    def open_activities():
        from activities import open_activities
        open_activities()

    def open_event_calendar():
        from event_calendar import open_calendar
        open_calendar(username)

    def open_bulletin():
        from bulletin import open_bulletin
        open_bulletin()

    def open_emergency():
        from emergency import open_emergency
        open_emergency()

    def open_reminders():
        from reminders import open_reminders
        open_reminders()

    tk.Button(root, text="Activities", width=20, command=open_activities).pack(pady=5)
    tk.Button(root, text="Event Calendar", width=20, command=open_event_calendar).pack(pady=5)
    tk.Button(root, text="Bulletin Board", width=20, command=open_bulletin).pack(pady=5)
    tk.Button(root, text="Emergency Contacts", width=20, command=open_emergency).pack(pady=5)
    tk.Button(root, text="Reminders", width=20, command=open_reminders).pack(pady=5)  

    root.mainloop()
