from Model.database import User, Sessionlocal
import AppController
from View.LoginView import LoginView


class RegisterController:
    def __init__(self,main_app, view):
        self.main_app = main_app
        self.view = view

        self.view.register_button.configure(command=self.registration)
        self.view.back_button.configure(command=self.main_app.show_login)
    def registration(self):
        datas = {"nem megfelelő felhasználónév!": self.view.username,
                 "nem megfelelő jelszó!":self.view.password,
                 "nem megfelelő email!": self.view.email,
                 "nem megfelelő telefonszám!": self.view.phone}
        for key, entry_widget in datas.items():
            data = entry_widget.get()
            if not data:
                entry_widget.delete(0,"end")
                self.view.error_label.config(text=f"{key}")
                return
        entered_name = self.view.username.get()
        entered_password = self.view.password.get()
        entered_email = self.view.email.get()
        entered_phone = self.view.phone.get()
        self.user = User(name=entered_name, password=entered_password, email=entered_email,phone=entered_phone,role_id=1)
        with Sessionlocal() as session:
            session.add(self.user)
            session.commit()
            session.refresh(self.user)
            self.main_app.login.registration_label.configure(text="Successfully registered")
            self.main_app.show_login()
