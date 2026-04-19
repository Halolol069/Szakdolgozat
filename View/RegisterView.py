import customtkinter

class RegisterView(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Register")
        self.geometry("600x600")
        self.username_label = customtkinter.CTkLabel(self, text="Username")
        self.username_label.pack(padx=5, pady=5)

        self.username = customtkinter.CTkEntry(self, placeholder_text="Pl: John Doe", width=20, height=5)
        self.username.pack(padx=5, pady=5,fill="x")

        self.password_label = customtkinter.CTkLabel(self, text="Password")
        self.password_label.pack(padx=5, pady=5)

        self.password = customtkinter.CTkEntry(self, placeholder_text="Password", width=20, height=5, show='*')
        self.password.pack(padx=5, pady=5,fill="x")

        self.email_label = customtkinter.CTkLabel(self, text="Email")
        self.email_label.pack(padx=5, pady=5)

        self.email = customtkinter.CTkEntry(self, placeholder_text="Email", width=20, height=5)
        self.email.pack(padx=5, pady=5,fill="x")

        self.phone_label=customtkinter.CTkLabel(self, text="Phone Number")
        self.phone_label.pack(padx=5, pady=5)

        self.phone = customtkinter.CTkEntry(self, placeholder_text="Phone Number", width=20, height=5)
        self.phone.pack(padx=5, pady=5,fill="x")

        self.register_button = customtkinter.CTkButton(self,text="Register")
        self.register_button.pack(padx=5,pady=5)

registerView = RegisterView()
registerView.mainloop()