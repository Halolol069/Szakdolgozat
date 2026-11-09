import customtkinter

class DashboardView(customtkinter.CTkFrame):

    def change_appearence(self, new_appearence: str):
        if new_appearence == "Sötét":
            customtkinter.set_appearance_mode("Dark")
        else:
            customtkinter.set_appearance_mode("Light")

    def __init__(self,master):
        super().__init__(master)

        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(16, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Készletkezelő",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.parts_button = customtkinter.CTkButton(self.sidebar_frame, text="Alkatrészek")
        self.parts_button.grid(row=1, column=0, padx=20, pady=10)

        self.transaction_button = customtkinter.CTkButton(self.sidebar_frame, text="Raktármozgás")
        self.transaction_button.grid(row=2, column=0, padx=20, pady=10)

        self.compatibility_button = customtkinter.CTkButton(self.sidebar_frame, text="Kompatibilitás")
        self.compatibility_button.grid(row=3, column=0, padx=20, pady=10)

        self.admin_button = customtkinter.CTkButton(self.sidebar_frame, text="Admin Panel")
        self.admin_button.grid(row=4, column=0, padx=20, pady=10)

        self.export_pdf_button = customtkinter.CTkButton(self.sidebar_frame, text="PDF Export")
        self.export_pdf_button.grid(row=5, column=0, padx=20, pady=10)

        self.export_csv_button = customtkinter.CTkButton(self.sidebar_frame, text="CSV Export")
        self.export_csv_button.grid(row=6, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Megjelenés:", anchor="w")
        self.appearance_mode_label.grid(row=12, column=0, padx=20, pady=(10,0))

        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Világos","Sötét"], command=self.change_appearence)
        self.appearance_mode_optionmenu.grid(row=13, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionmenu.set("Világos")

        self.logout_button = customtkinter.CTkButton(self.sidebar_frame, text="Kijelentkezés",
                                                     fg_color="red", hover_color="darkred")
        self.logout_button.grid(row=14, column=0, padx=20, pady=20, sticky="s")

        self.back_button = customtkinter.CTkButton(self.sidebar_frame,text="Vissza")

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        self.welcome_label = customtkinter.CTkLabel(self.main_frame, text="Üdvözöllek a Rendszerben!",
                                                    font=customtkinter.CTkFont(size=24, weight="bold"))
        self.welcome_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.stats_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.card1 = customtkinter.CTkFrame(self.stats_frame, corner_radius=10, fg_color="#1f538d")
        self.card1.grid(row=0, column=0, padx=10, sticky="ew")
        self.card1_title = customtkinter.CTkLabel(self.card1, text="Nyilvántartott Alkatrészek", text_color="white", font=customtkinter.CTkFont(size=14))
        self.card1_title.pack(pady=(15, 0))
        self.card1_value = customtkinter.CTkLabel(self.card1, text="- db", text_color="white", font=customtkinter.CTkFont(size=26, weight="bold"))
        self.card1_value.pack(pady=(0, 15))

        self.card2 = customtkinter.CTkFrame(self.stats_frame, corner_radius=10, fg_color="#166534")
        self.card2.grid(row=0, column=1, padx=10, sticky="ew")
        self.card2_title = customtkinter.CTkLabel(self.card2, text="Raktárkészlet Értéke", text_color="white", font=customtkinter.CTkFont(size=14))
        self.card2_title.pack(pady=(15, 0))
        self.card2_value = customtkinter.CTkLabel(self.card2, text="- Ft", text_color="white", font=customtkinter.CTkFont(size=26, weight="bold"))
        self.card2_value.pack(pady=(0, 15))

        self.card3 = customtkinter.CTkFrame(self.stats_frame, corner_radius=10, fg_color="#991b1b")
        self.card3.grid(row=0, column=2, padx=10, sticky="ew")
        self.card3_title = customtkinter.CTkLabel(self.card3, text="Kritikus Készletszinten", text_color="white", font=customtkinter.CTkFont(size=14))
        self.card3_title.pack(pady=(15, 0))
        self.card3_value = customtkinter.CTkLabel(self.card3, text="- db", text_color="white", font=customtkinter.CTkFont(size=26, weight="bold"))
        self.card3_value.pack(pady=(0, 15))

        self.chart_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=10, fg_color="gray20")
        self.chart_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")