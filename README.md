Engineering Productivity App

This project is a Tkinter-based desktop application designed for engineers and students to manage tasks, events, announcements, and quick contacts. It combines productivity features with CRUD operations and a user-friendly interface.

Features

User Authentication
Login and registration system for personalized use.

Dashboard
Central navigation hub for all features.

Activities Manager
Create, view, edit, and delete weekly tasks and schedules. Includes reminders for upcoming tasks.

Event Calendar
Display and organize events. Announcements from the bulletin board are automatically posted here.

Bulletin Board
Post and browse announcements. Integrated with the event calendar for visibility.

Emergency Contacts
Quick access buttons for security, counseling, health services, and other essential contacts.

Reminders
Notifications for important tasks and events.

Technology Stack

Frontend: Python with Tkinter for the GUI

Backend: SQLite3 for local data persistence

Architecture: Modular design with separate files for activities, bulletin board, calendar, and dashboard

Purpose

The application demonstrates CRUD functionality, modular Python development, and database integration in a practical productivity tool. It is suitable for engineers, students, or organizations that need a simple desktop application for task management, announcements, and quick access to critical information.

How to Run

Clone the repository
Clone the repository to your local machine and navigate to the project folder.

Set up a virtual environment (recommended)
Create a virtual environment to manage dependencies.
On Windows: python -m venv virt
Activate it: .\virt\Scripts\activate
On Mac/Linux: python -m venv virt
Activate it: source virt/bin/activate

Install dependencies
Install all required Python packages using pip. 
tkinter
tkcalendar

Initialize the database
Run db_setup.py once to create all necessary tables.

Run the application
Launch the app by running main.py.

Login or register a new account
Use the login screen to access the dashboard, or register a new account if you are a first-time user.
