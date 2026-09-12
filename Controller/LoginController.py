import bcrypt

from Model.database import User, Sessionlocal

class LoginController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view
        self.view.login_button.configure(command=self.login)
    def login(self):
        datas = {"username": self.view.username,
                 "password": self.view.password,
                 }
        for key, values in datas.items():
            data = values.get()
            if not data:
                values.delete(0, "end")
                self.view.error_label.configure(text=f"The {key} is empty, please fill the entries", fg_color="red")
                return
        entered_name = self.view.username.get()
        entered_password = self.view.password.get()
        with Sessionlocal() as session:
            self.user = session.query(User).filter_by(name=entered_name).first()
            if not self.user:
                self.view.username.delete(0,"end")
                self.view.password.delete(0,"end")
                self.view.error_label.configure(text=f"User not found", fg_color="red")
                return
            elif not bcrypt.checkpw(entered_password.encode("utf-8"), self.user.password.encode("utf-8")):
                self.view.username.delete(0, "end")
                self.view.password.delete(0, "end")
                self.view.error_label.configure(text=f"The data is invalid please try again.", fg_color="red")
                return

            self.view.username.delete(0, "end")
            self.view.password.delete(0, "end")
            self.view.error_label.configure(text="")
            self.main_app.show_dashboard()

            print("Sikeres belépés!")

            self.main_app.dashboard_controller.check_inventory_alerts()