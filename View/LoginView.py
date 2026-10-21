import customtkinter
class LoginView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.registration_label = customtkinter.CTkLabel(self,text='')
        self.registration_label.pack(fill='x')

        self.error_label = customtkinter.CTkLabel(self,text='')
        self.error_label.pack(fill='x')

        self.username_label = customtkinter.CTkLabel(self,text="Username/Email:")
        self.username_label.pack(padx=4, pady=5, fill="x")

        self.username = customtkinter.CTkEntry(self,placeholder_text="Username/Email", width=120, height=20)
        self.username.pack(padx=5,pady=5, fill="x")

        self.password_label= customtkinter.CTkLabel(self, text="Password:")
        self.password_label.pack(padx=4, pady=5, fill="x")

        self.password = customtkinter.CTkEntry(self,placeholder_text="Password", width=120, height=20, show="*")
        self.password.pack(padx=5,pady=5, fill="x")

        self.show_password_checkbox = customtkinter.CTkCheckBox(self, text="Jelszó megjelenítése",command=self.toggle_password)
        self.show_password_checkbox.pack(padx=5, pady=5, fill="x")

        self.register_button = customtkinter.CTkButton(self,text="Register")
        self.register_button.pack(padx=5,pady=5)

        self.login_button = customtkinter.CTkButton(self,text="Login")
        self.login_button.pack(padx=5)

    def toggle_password(self):
        if self.show_password_checkbox.get() == 1:
            self.password.configure(show='')
        else:
            self.password.configure(show='*')