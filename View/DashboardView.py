import customtkinter

class DashboardView(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)  # Ez tolja le a kijelentkezés gombot az aljára

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Készletkezelő",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.parts_button = customtkinter.CTkButton(self.sidebar_frame, text="Alkatrészek")
        self.parts_button.grid(row=1, column=0, padx=20, pady=10)

        self.logout_button = customtkinter.CTkButton(self.sidebar_frame, text="Kijelentkezés", fg_color="#d32f2f",
                                                     hover_color="#b71c1c")
        self.logout_button.grid(row=5, column=0, padx=20, pady=20, sticky="s")

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.welcome_label = customtkinter.CTkLabel(self.main_frame, text="Üdvözöllek a Rendszerben!", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.welcome_label.pack(pady=50)