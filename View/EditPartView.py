import customtkinter

class EditPartView(customtkinter.CTkToplevel):
    def __init__(self, master,manufacturer_dict):
        super().__init__(master)

        self.title("Alkatrész Szerkesztése")
        self.geometry("460x680")

        self.attributes("-topmost", True)

        self.manufacturer_dict = manufacturer_dict

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, corner_radius=10)
        self.scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.title_label = customtkinter.CTkLabel(self.scrollable_frame, text="Alkatrész Szerkesztése",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(10, 20))

        self.part_number = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Cikkszám", height=36)
        self.part_number.pack(pady=6, padx=20, fill="x")

        self.name = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Megnevezés", height=36)
        self.name.pack(pady=6, padx=20, fill="x")

        self.type = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Típus", height=36)
        self.type.pack(pady=6, padx=20, fill="x")

        self.price = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Ár (Ft)", height=36)
        self.price.pack(pady=6, padx=20, fill="x")

        self.amount = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Készlet mennyiség", height=36)
        self.amount.pack(pady=6, padx=20, fill="x")

        self.min_amount = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Minimum mennyiség", height=36)
        self.min_amount.pack(pady=6, padx=20, fill="x")

        self.max_amount = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Maximum mennyiség", height=36)
        self.max_amount.pack(pady=6, padx=20, fill="x")

        self.manufacturer_names = list(self.manufacturer_dict.keys())
        self.manufacturer_combobox = customtkinter.CTkComboBox(self.scrollable_frame, values=self.manufacturer_names,height=36, state="readonly")
        self.manufacturer_combobox.pack(pady=6, padx=20, fill="x")
        self.manufacturer_combobox.set("Válasz egy gyártót...")

        self.image_label = customtkinter.CTkLabel(self.scrollable_frame, text="Nincs kép", width=150, height=150, bg_color="gray", corner_radius=10)
        self.image_label.pack(pady=(15,10), padx=20)

        self.upload_button = customtkinter.CTkButton(self.scrollable_frame, text="Kép feltöltése", fg_color="gray40", hover_color="gray30", height=34)
        self.upload_button.pack(pady=5, padx=60,fill="x")

        self.save_button = customtkinter.CTkButton(self.scrollable_frame, text="Módosítások Mentése", fg_color="#1f538d", hover_color="#14375e", height=42, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.save_button.pack(pady=(20,15), padx=20, fill="x")