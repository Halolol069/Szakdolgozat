import customtkinter

class RegisterView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.card = customtkinter.CTkFrame(self, width=400, corner_radius=15)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = customtkinter.CTkLabel(self.card, text="Új fiók létrehozása", font=customtkinter.CTkFont(size=22, weight="bold"))
        self.title_label.pack(padx=40, pady=(25, 10))

        self.error_label = customtkinter.CTkLabel(self.card, text='', font=customtkinter.CTkFont(size=12, weight="bold"))
        self.error_label.pack(fill="x", padx=30, pady=(0,5))

        self.username_label = customtkinter.CTkLabel(self.card, text="Felhasználónév:", anchor="w", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.username_label.pack(padx=30, pady=(5,2), fill="x")

        self.username = customtkinter.CTkEntry(self.card, placeholder_text="Pl: John Doe", width=320, height=36)
        self.username.pack(padx=30, pady=(0,10),fill="x")

        self.password_label = customtkinter.CTkLabel(self.card, text="Jelszó",anchor="w", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.password_label.pack(padx=30, pady=(5,2), fill="x")

        self.password = customtkinter.CTkEntry(self.card, placeholder_text="Minimum 6 karakter", width=320, height=36, show='*')
        self.password.pack(padx=30, pady=(0,10),fill="x")

        self.email_label = customtkinter.CTkLabel(self.card, text="E-mail cím:", anchor="w", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.email_label.pack(padx=30, pady=(5,2), fill="x")

        self.email = customtkinter.CTkEntry(self.card, placeholder_text="pelda@gmail.com", width=320, height=36)
        self.email.pack(padx=30, pady=(0,10),fill="x")

        self.phone_label=customtkinter.CTkLabel(self.card, text="Telefonszám:",anchor="w", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.phone_label.pack(padx=30, pady=(5,2), fill="x")

        self.phone = customtkinter.CTkEntry(self.card, placeholder_text="+36204215487", width=320, height=36)
        self.phone.pack(padx=30, pady=(0,20),fill="x")

        self.back_button = customtkinter.CTkButton(self.card,text="Visszalépés", height=36, fg_color="gray35", hover_color="gray25")
        self.back_button.pack(padx=30,pady=(0,25), fill="x")

        self.register_button = customtkinter.CTkButton(self.card,text="Regisztráció", height=40, fg_color="green", hover_color="darkgreen", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.register_button.pack(padx=30,pady=(0,10), fill="x")

    def clear_form(self):
        datas = [self.username, self.password, self.email, self.phone]
        for data in datas:
            data.delete(0, "end")