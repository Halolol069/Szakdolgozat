import customtkinter


class AddPartView(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Új Alkatrész Hozzáadása")
        self.geometry("460x680")

        self.attributes("-topmost", True)
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, corner_radius=10)
        self.scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.title_label = customtkinter.CTkLabel(self.scrollable_frame, text="Új Alkatrész",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(10, 20))

        self.part_number = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Cikkszám (pl. 1J0907319C)", height=36)
        self.part_number.pack(pady=6, padx=20, fill="x")

        self.name = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Megnevezés (pl. Fékbetét)", height=36)
        self.name.pack(pady=6, padx=20, fill="x")

        self.type = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Típus (pl. Fékrendszer)", height=36)
        self.type.pack(pady=6, padx=20, fill="x")

        self.manufacturer_id = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Gyártó ID (pl. 1)", height=36)
        self.manufacturer_id.pack(pady=6, padx=20, fill="x")

        self.price = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Ár (Ft)", height=36)
        self.price.pack(pady=6, padx=20, fill="x")

        self.amount = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Készlet mennyiség", height=36)
        self.amount.pack(pady=6, padx=20, fill="x")

        self.min_amount = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Minimum mennyiség", height=36)
        self.min_amount.pack(pady=6, padx=20, fill="x")

        self.max_amount = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Maximum mennyiség", height=36)
        self.max_amount.pack(pady=6, padx=20, fill="x")

        self.image_label = customtkinter.CTkLabel(self.scrollable_frame, text="Nincs kép", width=150, height=150, bg_color="gray")
        self.image_label.pack(pady=(15,10), padx=20)

        self.upload_button = customtkinter.CTkButton(self.scrollable_frame, text="Kép feltöltése")
        self.upload_button.pack(pady=5)

        self.save_button = customtkinter.CTkButton(self.scrollable_frame, text="Mentés", fg_color="green", height=42, hover_color="darkgreen",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.save_button.pack(pady=(20,15), padx=20, fill="x")