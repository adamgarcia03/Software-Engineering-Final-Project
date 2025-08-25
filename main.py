from login import show_login
from db_setup import init_db
if __name__ == "__main__":
    #ensure database is initialized
    init_db()
    show_login()


#Purpose: Entry point of the app. Ensures database is ready and launches login.