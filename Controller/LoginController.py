import bcrypt

from Model.database import User, Sessionlocal
from Controller.password_utils import is_password_too_long

class LoginController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view
        self.view.login_button.configure(command=self.login)

    def show_error(self,text):
        self.view.error_label.configure(text=text, text_color="red", fg_color="transparent")

    def login(self):
        login_name = self.view.username.get().strip()
        password = self.view.password.get()

        if not login_name or not password:
            self.show_error("Add meg a felhasználónevet és a jelszót!")
            return

        try:
            with Sessionlocal() as session:
                user = session.query(User).filter(
                    (User.name == login_name) | (User.email == login_name)
                ).first()
        except Exception as e:
            print("Adatbázis-kapcsolati hiba a bejelentkezéskor:", e)
            self.show_error("Nem sikerült csatlakozni az adatbázishoz!")
            return

        valid = (user is not None
                 and not is_password_too_long(password)
                 and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")))
        if not valid:
            self.view.password.delete(0, "end")
            self.show_error("Hibás felhasználónév vagy jelszó!")
            return

        if not getattr(user, "is_active", True):
            self.view.password.delete(0, "end")
            self.show_error("Ez a felhasználói fiók fel van függesztve!")
            return

        self.view.username.delete(0, "end")
        self.view.password.delete(0, "end")
        self.view.error_label.configure(text="", fg_color="transparent")
        self.main_app.current_user = user
        self.main_app.show_dashboard()
        self.main_app.dashboard_controller.check_inventory_alerts()