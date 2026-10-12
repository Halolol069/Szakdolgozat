import customtkinter

class DashboardView(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Készletkezelő",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.parts_button = customtkinter.CTkButton(self.sidebar_frame, text="Alkatrészek")
        self.parts_button.grid(row=1, column=0, padx=20, pady=10)

        self.transaction_button = customtkinter.CTkButton(self.sidebar_frame, text="Raktármozgás")
        self.transaction_button.grid(row=2, column=0, padx=20, pady=10)

        self.compatibility_button = customtkinter.CTkButton(self.sidebar_frame, text="Kompatibilitás")
        self.compatibility_button.grid(row=3, column=0, padx=20, pady=10)

        self.export_pdf_button = customtkinter.CTkButton(self.sidebar_frame, text="PDF Export")
        self.export_pdf_button.grid(row=4, column=0, padx=20, pady=10)

        self.logout_button = customtkinter.CTkButton(self.sidebar_frame, text="Kijelentkezés",
                                                     fg_color="red", hover_color="darkred")
        self.logout_button.grid(row=10, column=0, padx=20, pady=20, sticky="s")

        self.back_button = customtkinter.CTkButton(self.sidebar_frame,text="Vissza")

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.welcome_label = customtkinter.CTkLabel(self.main_frame, text="Üdvözöllek a Rendszerben!",
                                                    font=customtkinter.CTkFont(size=24, weight="bold"))
        self.welcome_label.pack(pady=50)