from database import create_tables
from models.user import create_default_admin
from ui.login_window import LoginWindow


def main():
    create_tables()
    create_default_admin()

    login = LoginWindow()
    login.run()


if __name__ == "__main__":
    main()