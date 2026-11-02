import customtkinter
class LoginView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.card = customtkinter.CTkFrame(self, width=380, corner_radius=15)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = customtkinter.CTkLabel(self.card,text="Bejelentkezés", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.title_label.pack(padx=40, pady=(30, 5))

        self.subtitle_label = customtkinter.CTkLabel(self.card,text="Készletgazdálkodási Rendszer", font=customtkinter.CTkFont(size=13), text_color="gray70")
        self.subtitle_label.pack(padx=40, pady=(0, 15))

        self.error_label = customtkinter.CTkLabel(self.card,text='')
        self.error_label.pack(fill='x',padx=30, pady=(0,5))

        self.username_label = customtkinter.CTkLabel(self.card, text="Felhasználó/E-mail:", anchor="w", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.username_label.pack(padx=30, pady=(5, 2), fill="x")

        self.username = customtkinter.CTkEntry(self.card,placeholder_text="Felhasználó/E-mail", width=300, height=38)
        self.username.pack(padx=30,pady=(0, 12), fill="x")

        self.password_label= customtkinter.CTkLabel(self.card, text="Jelszó:", anchor="w", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.password_label.pack(padx=30, pady=(5,2), fill="x")

        self.password = customtkinter.CTkEntry(self.card,placeholder_text="Jelszó", width=300, height=38, show="*")
        self.password.pack(padx=30,pady=(0,10), fill="x")

        self.show_password_checkbox = customtkinter.CTkCheckBox(self.card, text="Jelszó megjelenítése",command=self.toggle_password, font=customtkinter.CTkFont(size=12))
        self.show_password_checkbox.pack(padx=30, pady=(0,20), anchor="w")

        self.login_button = customtkinter.CTkButton(self.card,text="Belépés", height=40, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.login_button.pack(padx=30, pady=(0,10), fill="x")

    def toggle_password(self):
        if self.show_password_checkbox.get() == 1:
            self.password.configure(show='')
        else:
            self.password.configure(show='*')