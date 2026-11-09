import customtkinter


class AddPartView(customtkinter.CTkToplevel):
    def __init__(self, master, manufacturer_dict):
        super().__init__(master)

        self.title("Új Alkatrész Hozzáadása")
        self.geometry("460x680")

        self.attributes("-topmost", True)
        self.manufacturer_dict = manufacturer_dict
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, corner_radius=10)
        self.scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.title_label = customtkinter.CTkLabel(self.scrollable_frame, text="Új Alkatrész",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(10, 20))

        self.part_number_label = customtkinter.CTkLabel(self.scrollable_frame, text="Cikkszám:", height=36, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.part_number_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.part_number = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Cikkszám (pl. 1J0907319C)", height=36)
        self.part_number.pack(pady=6, padx=20, fill="x")

        self.name_label = customtkinter.CTkLabel(self.scrollable_frame, text="Megnevezés:", height=36,font=customtkinter.CTkFont(size=20, weight="bold"))
        self.name_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.name = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Megnevezés (pl. Fékbetét)", height=36)
        self.name.pack(pady=6, padx=20, fill="x")

        self.type_label = customtkinter.CTkLabel(self.scrollable_frame, text="Típus:", height=36,font=customtkinter.CTkFont(size=20, weight="bold"))
        self.type_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.type = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Típus (pl. Fékrendszer)", height=36)
        self.type.pack(pady=6, padx=20, fill="x")

        self.location_label = customtkinter.CTkLabel(self.scrollable_frame, text="Polc:", height=36,font=customtkinter.CTkFont(size=20, weight="bold"))
        self.location_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.location = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="pl. A-sor, 3. polc", height=36)
        self.location.pack(pady=6, padx=20, fill="x")

        self.manufacturer_label = customtkinter.CTkLabel(self.scrollable_frame, text="Gyártó:", height=36,font=customtkinter.CTkFont(size=20, weight="bold"))
        self.manufacturer_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.manufacturer_names = list(self.manufacturer_dict.keys())
        self.manufacturer_combobox = customtkinter.CTkComboBox(self.scrollable_frame,values=self.manufacturer_names,height=36, state="readonly")
        self.manufacturer_combobox.pack(pady=6, padx=20, fill="x")
        self.manufacturer_combobox.set("Válasz egy gyártót...")

        self.price_label = customtkinter.CTkLabel(self.scrollable_frame, text="Ár:", height=36,font=customtkinter.CTkFont(size=20, weight="bold"))
        self.price_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.price = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Ár (Ft)", height=36)
        self.price.pack(pady=6, padx=20, fill="x")

        self.amount_label = customtkinter.CTkLabel(self.scrollable_frame, text="Készlet mennyiség:", height=36,font=customtkinter.CTkFont(size=20, weight="bold"))
        self.amount_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.amount = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Készlet mennyiség", height=36)
        self.amount.pack(pady=6, padx=20, fill="x")

        self.min_amount_label = customtkinter.CTkLabel(self.scrollable_frame, text="Minimum mennyiség:", height=36,font=customtkinter.CTkFont(size=20, weight="bold"))
        self.min_amount_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.min_amount = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Minimum mennyiség", height=36)
        self.min_amount.pack(pady=6, padx=20, fill="x")

        self.max_amount_label = customtkinter.CTkLabel(self.scrollable_frame, text="Maximum mennyiség:", height=36,font=customtkinter.CTkFont(size=20, weight="bold"))
        self.max_amount_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.max_amount = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Maximum mennyiség", height=36)
        self.max_amount.pack(pady=6, padx=20, fill="x")

        self.image_label = customtkinter.CTkLabel(self.scrollable_frame, text="Nincs kép", width=150, height=150, bg_color="gray")
        self.image_label.pack(pady=(15,10), padx=20)

        self.upload_button = customtkinter.CTkButton(self.scrollable_frame, text="Kép feltöltése")
        self.upload_button.pack(pady=5)

        self.save_button = customtkinter.CTkButton(self.scrollable_frame, text="Mentés", fg_color="green", height=42, hover_color="darkgreen",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.save_button.pack(pady=(20,15), padx=20, fill="x")