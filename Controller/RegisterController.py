import bcrypt

from Model.database import User, Sessionlocal

class RegisterController:
    def __init__(self,main_app, view):
        self.main_app = main_app
        self.view = view
        self.view.register_button.configure(command=self.registration)
        self.view.back_button.configure(command=self.main_app.show_login)

    def registration(self):
        datas = {"felhasználónév": self.view.username,
                 "jelszó":self.view.password,
                 "email": self.view.email,
                 "telefonszám": self.view.phone}
        for key, entry_widget in datas.items():
            data = entry_widget.get()
            if not data:
                entry_widget.delete(0,"end")
                self.view.error_label.configure(text=f"A(z) {key} mező üres, kérlek töltsd ki!", text_color="red",fg_color="transparent")
                return

            elif key=="email" and ("@" not in data or "." not in data):
                entry_widget.delete(0,"end")
                self.view.error_label.configure(text=f"A(z) {key} nem megfelelő, kérlek használj: @ és . kitöltéskor!",text_color="red",fg_color="transparent")
                return

            elif key=="jelszó" and (6 > len(data)):
                entry_widget.delete(0,"end")
                self.view.error_label.configure(text=f"A(z) {key} túl rövid, minimum 6 karaktert kell használni!", text_color="red",fg_color="transparent")
                return

            elif key=="telefonszám" and not data.lstrip("+").isdigit():
                entry_widget.delete(0,"end")
                self.view.error_label.configure(text=f"A(z) {key} helytelen, használj számokat! (lehet + kezdeni!)", text_color="red",fg_color="transparent")
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
                self.main_app.login.registration_label.configure(text="Sikeres regisztráció!", fg_color="green")
                self.main_app.show_login()
            except Exception as e:
                session.rollback()
                error = str(e).lower()
                if "users_name_key" in error or "users.name" in error:
                    self.view.error_label.configure(text="Ez a felhasználónév már foglalt!", text_color="red")
                elif "users_email_key" in error or "users.email" in error:
                    self.view.error_label.configure(text="Ez az e-mail cím már regisztrálva van!", text_color="red")
                elif "users_phone_key" in error or "users.phone" in error:
                    self.view.error_label.configure(text="Ez a telefonszám már regisztrálva van!", text_color="red")
                else:
                    self.view.error_label.configure(text="Váratlan hiba történt a mentés során!", text_color="red")
                    print("Adatbázis hiba:", error)