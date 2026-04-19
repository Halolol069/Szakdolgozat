import customtkinter

class LoginView(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("600x600")

        self.username_label = customtkinter.CTkLabel(self,text="Username:")
        self.username_label.pack(padx=4, pady=5, fill="x")

        self.username = customtkinter.CTkEntry(self,placeholder_text="Username", width=120, height=20)
        self.username.pack(padx=5,pady=5, fill="x")

        self.password_label= customtkinter.CTkLabel(self, text="Password:")
        self.password_label.pack(padx=4, pady=5, fill="x")

        self.password = customtkinter.CTkEntry(self,placeholder_text="Password", width=120, height=20, show="*")
        self.password.pack(padx=5,pady=5, fill="x")

        self.register_button = customtkinter.CTkButton(self,text="Register") #command=register
        self.register_button.pack(padx=5,pady=5)

        self.login_button = customtkinter.CTkButton(self,text="Login") #command=login
        self.login_button.pack(padx=5)
loginView = LoginView()
loginView.mainloop()