from tkinter import ttk

import customtkinter

class TransactionView(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self.transaction_type_menu = customtkinter.CTkOptionMenu(self, values=["Bevételezés", "Kiadás"])
        self.transaction_type_menu.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.transaction_quantity_menu = customtkinter.CTkEntry(self, placeholder_text="Mennyiség (pl. 5)")
        self.transaction_quantity_menu.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        self.search_bar = customtkinter.CTkEntry(self, placeholder_text="Keresés név vagy cikkszám alapján")
        self.search_bar.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.filter_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.filter_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.filter_frame.grid_columnconfigure((0,1,2,4), weight=1)
        self.filter_frame.grid_columnconfigure(3, weight=2)

        self.vehicletype_dropdown = customtkinter.CTkOptionMenu(self.filter_frame, values=["Jármű típus"])
        self.vehicletype_dropdown.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")
        self.vehicletype_dropdown.set("Jármű típus")

        self.brand_dropdown = customtkinter.CTkOptionMenu(self.filter_frame, values=["Márka"])
        self.brand_dropdown.grid(row=0, column=1, padx=20, pady=5, sticky="nsew")
        self.brand_dropdown.set("Márka")

        self.model_dropdown = customtkinter.CTkOptionMenu(self.filter_frame, values=["Modell"])
        self.model_dropdown.grid(row=0, column=2, padx=20, pady=5, sticky="nsew")
        self.model_dropdown.set("Modell")

        self.engine_dropdown = customtkinter.CTkOptionMenu(self.filter_frame, values=["Motor"], dynamic_resizing=False, width=250)
        self.engine_dropdown.grid(row=0, column=3, padx=20, pady=5, sticky="nsew")
        self.engine_dropdown.set("Motor")

        self.reset_filter_button = customtkinter.CTkButton(master=self.filter_frame, text="Szűrők törlése", fg_color="gray40", hover_color="gray30")
        self.reset_filter_button.grid(row=0, column=4, padx=20, pady=5, sticky="nsew")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="gray20", foreground="white", rowheight=25, fieldbackground="gray20",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', 'blue')])
        style.configure("Treeview.Heading", background="gray30", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', 'gray40')])
        self.transaction_tree = ttk.Treeview(self, selectmode="browse", columns=("Part_id","Part_number","Name","Quantity","Type","Price"), show="headings", style="Treeview")
        self.transaction_tree.heading("Part_id", text="Azonosító")
        self.transaction_tree.heading("Part_number", text="Cikkszám")
        self.transaction_tree.heading("Name", text="Név")
        self.transaction_tree.heading("Quantity", text="Mennyiség")
        self.transaction_tree.heading("Type", text="Típus")
        self.transaction_tree.heading("Price", text="Ár")
        self.transaction_tree.column("Part_id", width=60, anchor="center")
        self.transaction_tree.column("Part_number", width=120, anchor="center")
        self.transaction_tree.column("Name", width=250, anchor="w")
        self.transaction_tree.column("Quantity", width=80, anchor="center")
        self.transaction_tree.column("Type", width=100, anchor="center")
        self.transaction_tree.column("Price", width=80, anchor="center")
        self.transaction_tree.grid(row=2, columnspan=3, padx=20, pady=20, sticky="nsew")

        self.to_cart_save_button = customtkinter.CTkButton(master=self, text="Kosárba")
        self.to_cart_save_button.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

        self.cart_review_button = customtkinter.CTkButton(master=self, text="Kosár megtekintése")
        self.cart_review_button.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")

        self.log_label=customtkinter.CTkLabel(master=self, text="Legutóbbi készletmozgások: ", font=("Arial", 14, "bold"))
        self.log_label.grid(row=4, column=0, columnspan=3, padx=20, pady=(20,5), sticky="nsew")

        self.history_tree = ttk.Treeview(self, selectmode="none", columns=("Log_id","Date","Type","Part","Qty","User"),show="headings", style="Treeview", height=7)

        self.history_tree.heading("Log_id", text="ID")
        self.history_tree.heading("Date", text="Dátum")
        self.history_tree.heading("Type", text="Művelet")
        self.history_tree.heading("Part", text="Alkatrész")
        self.history_tree.heading("Qty", text="Változás")
        self.history_tree.heading("User", text="Felhasználó")

        self.history_tree.column("Log_id", width=50, anchor="center")
        self.history_tree.column("Date", width=140, anchor="center")
        self.history_tree.column("Type", width=100, anchor="center")
        self.history_tree.column("Part", width=250, anchor="w")
        self.history_tree.column("Qty", width=80, anchor="center")
        self.history_tree.column("User", width=120, anchor="center")

        self.history_tree.grid(row=5,column=0,columnspan=3,padx=20,pady=20,sticky="nsew")

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(5, weight=1)