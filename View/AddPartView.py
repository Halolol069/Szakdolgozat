import customtkinter


class AddPartView(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Új Alkatrész Hozzáadása")
        self.geometry("400x550")

        self.attributes("-topmost", True)

        self.title_label = customtkinter.CTkLabel(self, text="Új Alkatrész",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        self.part_number = customtkinter.CTkEntry(self, placeholder_text="Cikkszám (pl. 1J0907319C)")
        self.part_number.pack(pady=10, padx=20, fill="x")

        self.name = customtkinter.CTkEntry(self, placeholder_text="Megnevezés (pl. Fékbetét)")
        self.name.pack(pady=10, padx=20, fill="x")

        self.type = customtkinter.CTkEntry(self, placeholder_text="Típus (pl. Fékrendszer)")
        self.type.pack(pady=10, padx=20, fill="x")

        self.price = customtkinter.CTkEntry(self, placeholder_text="Ár (Ft)")
        self.price.pack(pady=10, padx=20, fill="x")

        self.amount = customtkinter.CTkEntry(self, placeholder_text="Készlet mennyiség")
        self.amount.pack(pady=10, padx=20, fill="x")

        self.manufacturer_id = customtkinter.CTkEntry(self, placeholder_text="Gyártó ID (pl. 1)")
        self.manufacturer_id.pack(pady=10, padx=20, fill="x")

        self.save_button = customtkinter.CTkButton(self, text="Mentés", fg_color="green", hover_color="darkgreen")
        self.save_button.pack(pady=30)