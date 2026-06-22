import customtkinter
from tkinter import ttk


class PartsView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.title_label = customtkinter.CTkLabel(self.top_frame, text="Alkatrészek Kezelése", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.pack(side="left")

        self.delete_button = customtkinter.CTkButton(self.top_frame, text="Törlés", fg_color="red", hover_color="darkred", width=100)
        self.delete_button.pack(side="right", padx=5)

        self.edit_button = customtkinter.CTkButton(self.top_frame, text="Módosítás", width=100)
        self.edit_button.pack(side="right", padx=5)

        self.add_button = customtkinter.CTkButton(self.top_frame, text="Új Hozzáadása", fg_color="green", hover_color="darkgreen", width=120)
        self.add_button.pack(side="right", padx=5)

        self.table_frame = customtkinter.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="gray20", foreground="white", rowheight=25, fieldbackground="gray20",borderwidth=0)
        style.map('Treeview', background=[('selected', 'blue')])
        style.configure("Treeview.Heading", background="gray30", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', 'gray40')])

        columns = ("id", "part_number", "name", "type", "price", "amount")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", style="Treeview")

        self.tree.heading("id", text="ID")
        self.tree.heading("part_number", text="Cikkszám")
        self.tree.heading("name", text="Megnevezés")
        self.tree.heading("type", text="Típus")
        self.tree.heading("price", text="Ár (Ft)")
        self.tree.heading("amount", text="Készlet")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("part_number", width=150)
        self.tree.column("name", width=200)
        self.tree.column("type", width=100)
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("amount", width=80, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = customtkinter.CTkScrollbar(self.table_frame, command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)