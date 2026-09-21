from tkinter import ttk

import customtkinter

class TransactionView(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self.transaction_type_menu = customtkinter.CTkOptionMenu(self, values=["Bevételezés", "Kiadás"])
        self.transaction_type_menu.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.transaction_quantity_menu = customtkinter.CTkEntry(self)
        self.transaction_quantity_menu.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        self.search_bar = customtkinter.CTkEntry(self, placeholder_text="Keresés")
        self.search_bar.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="gray20", foreground="white", rowheight=25, fieldbackground="gray20",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', 'blue')])
        style.configure("Treeview.Heading", background="gray30", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', 'gray40')])
        self.transaction_tree = ttk.Treeview(self, selectmode="extended", columns=("Part_id","Name","Quantity",), show="headings", style="Treeview")
        self.transaction_tree.heading("Part_id", text="Alkatrész ID")
        self.transaction_tree.heading("Name", text="Név")
        self.transaction_tree.heading("Quantity", text="Mennyiség")
        self.transaction_tree.grid(row=2, columnspan=3, padx=20, pady=20, sticky="nsew")

        self.save_button = customtkinter.CTkButton(master=self, text="Mentés")
        self.save_button.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")