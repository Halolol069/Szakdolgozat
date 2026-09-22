import bcrypt

from Model.database import User, Sessionlocal
class RegisterController:
    def __init__(self,main_app, view):
        self.main_app = main_app
        self.view = view
        self.view.register_button.configure(command=self.registration)
        self.view.back_button.configure(command=self.main_app.show_login)

    def registration(self):
        datas = {"username": self.view.username,
                 "password":self.view.password,
                 "email": self.view.email,
                 "phone": self.view.phone}
        for key, entry_widget in datas.items():
            data = entry_widget.get()
            if not data:
                entry_widget.delete(0,"end")
                self.view.error_label.configure(text=f"The {key} is empty, please fill the entries", fg_color="red")
                return

            elif key=="email" and ("@" not in data or "." not in data):
                entry_widget.delete(0,"end")
                self.view.error_label.configure(text=f"The {key} is invalid, please use @ and . to fill the entries", fg_color="red")
                return

            elif key=="password" and (6 > len(data)):
                entry_widget.delete(0,"end")
                self.view.error_label.configure(text=f"The {key} is too short, please use at least 6 characters", fg_color="red")
                return

            elif key=="phone" and not data.replace("+","").isdigit():
                entry_widget.delete(0,"end")
                self.view.error_label.configure(text=f"The {key} is invalid, please use numbers!", fg_color="red")
                return

        entered_name = self.view.username.get()
        entered_password = self.view.password.get()
        entered_email = self.view.email.get()
        entered_phone = self.view.phone.get()
        hashed_password = bcrypt.hashpw(entered_password.encode("utf-8"), bcrypt.gensalt())

        self.user = User(name=entered_name, password=hashed_password.decode("utf-8"), email=entered_email,phone=entered_phone,role_id=2)

        with Sessionlocal() as session:
            try:
                session.add(self.user)
                session.commit()
                session.refresh(self.user)
                self.view.clear_form()
                self.main_app.login.registration_label.configure(text="Successfully registered", fg_color="green")
                self.main_app.show_login()
            except Exception as e:
                session.rollback()
                error = str(e).lower()
                entered_data = {"name":self.user.name, "email":self.user.email, "phone":self.user.phone}
                for key, data in entered_data.items():
                    if key in error:
                        self.view.error_label.configure(text=f"The {key} is already registered", fg_color="red")
                        break
