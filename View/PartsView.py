import customtkinter
from tkinter import ttk


class PartsView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.top_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,10), sticky="ew")

        self.title_label = customtkinter.CTkLabel(self.top_frame, text="Alkatrészek Kezelése", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.pack(side="left", padx=(0,20))

        self.search_entry = customtkinter.CTkEntry(self.top_frame, placeholder_text="Gyorskeresés név vagy cikkszám alapján...", width=280, height=35)
        self.search_entry.pack(side="left", padx=10)

        self.delete_button = customtkinter.CTkButton(self.top_frame, text="Törlés", fg_color="red", hover_color="darkred", width=100,height=35)
        self.delete_button.pack(side="right", padx=5)

        self.edit_button = customtkinter.CTkButton(self.top_frame, text="Módosítás", width=110, height=35)
        self.edit_button.pack(side="right", padx=5)

        self.add_button = customtkinter.CTkButton(self.top_frame, text="Új Hozzáadása", fg_color="green", hover_color="darkgreen", width=100, height=35)
        self.add_button.pack(side="right", padx=5)

        self.table_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.table_frame.grid(row=1, column=0, padx=(20,10), pady=(0, 20), sticky="nsew")
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="gray20", foreground="white", rowheight=25, fieldbackground="gray20",borderwidth=0)
        style.map('Treeview', background=[('selected', 'blue')])
        style.configure("Treeview.Heading", background="gray30", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', 'gray40')])

        columns = ("id", "part_number", "name", "type", "price", "amount", "recommended")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", style="Treeview")

        self.tree.heading("id", text="ID")
        self.tree.heading("part_number", text="Cikkszám")
        self.tree.heading("name", text="Megnevezés")
        self.tree.heading("type", text="Típus")
        self.tree.heading("price", text="Ár (Ft)")
        self.tree.heading("amount", text="Készlet")
        self.tree.heading("recommended", text="Ajánlott Rendelés")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("part_number", width=150)
        self.tree.column("name", width=200)
        self.tree.column("type", width=100)
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("amount", width=80, anchor="center")
        self.tree.column("recommended", width=120, anchor="center")

        self.tree.grid(row=0, column=0, padx=(0,10), pady=10, sticky="nsew")

        self.scrollbar = customtkinter.CTkScrollbar(self.table_frame, command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, padx=5, pady=10, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.preview_frame = customtkinter.CTkFrame(self, width=250, corner_radius=10)
        self.preview_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 20), sticky="nsew")
        self.preview_frame.grid_propagate(False)

        self.preview_title = customtkinter.CTkLabel(self.preview_frame, text="Termékfotó", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.preview_title.pack(pady=(20, 10), padx=15)

        self.image_container = customtkinter.CTkFrame(self.preview_frame, width=200, height=200, fg_color="gray25",corner_radius=10)
        self.image_container.pack(pady=10, padx=20)
        self.image_container.pack_propagate(False)

        self.preview_image_label = customtkinter.CTkLabel(self.image_container, text="Válassz ki egy\nalkatrészt a listából",width=200, height=200, fg_color="gray25", corner_radius=10)
        self.preview_image_label.pack(pady=10, padx=20)

        self.preview_name_label = customtkinter.CTkLabel(self.preview_frame, text="", font=customtkinter.CTkFont(size=14, weight="bold"), wraplength=210)
        self.preview_name_label.pack(pady=(10, 5), padx=15)

        self.preview_info_label = customtkinter.CTkLabel(self.preview_frame, text="", font=customtkinter.CTkFont(size=12), text_color="red", justify="left")
        self.preview_info_label.pack(pady=5, padx=15)

        legend_frame = customtkinter.CTkFrame(self.preview_frame, fg_color="gray25", corner_radius=8)
        legend_frame.pack(side="bottom", fill="x", padx=15, pady=15)

        customtkinter.CTkLabel(legend_frame, text="Készletszint jelölések:", font=customtkinter.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(8, 2))
        customtkinter.CTkLabel(legend_frame, text="* Kritikus (Min. alatt)", text_color="#ef4444", font=customtkinter.CTkFont(size=12)).pack(anchor="w", padx=10)
        customtkinter.CTkLabel(legend_frame, text="* Optimális / Magas", text_color="#22c55e", font=customtkinter.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(0, 8))