from tkinter import ttk, messagebox
import customtkinter

class CompatibilityView(customtkinter.CTkFrame):
    def search_action(self):
        self.selected_engine = self.engine_dropdown.get()
        if self.selected_engine == "":
            messagebox.showerror("Error", "Please select an engine")
            return
        self.controller.gets_parts_by_engine(self.selected_engine)

    def show_no_part_msgb(self):
        messagebox.showinfo("NoParts", "No parts for the engine")

    def save_action(self):
        if (self.vehiclebrand_dropdown.get() == "Márka" or self.model_dropdown.get() == "Modell"  or
                self.engine_dropdown.get() == "Motor"):
            messagebox.showerror("Hiba", "Kérlek válassz ki egy autót és motort a szűrőben a mentésehez!")
            return
        self.controller.save_compatibility()

    def delete_action(self):
        if (self.vehiclebrand_dropdown.get() == "Márka" or self.model_dropdown.get() == "Modell" or
                self.engine_dropdown.get() == "Motor"):
            messagebox.showerror("Hiba", "Kérlek válassz ki egy autót és motort a szűrőben a törléshez!")
            return
        self.controller.delete_compatibility()

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.car_filter = customtkinter.CTkFrame(self, width=280, corner_radius=10)
        self.car_filter.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="nsew")

        self.car_filter_label = customtkinter.CTkLabel(self.car_filter, text="Jármű kiválasztása", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.car_filter_label.pack(padx=25, pady=(20, 15))

        type_lbl = customtkinter.CTkLabel(self.car_filter, text="Jármű kategória:",anchor="w")
        type_lbl.pack(fill="x", padx=20, pady=(5, 2))
        self.vehicletype_dropdown = customtkinter.CTkOptionMenu(self.car_filter, values=["Jármű típus"], height=35)
        self.vehicletype_dropdown.pack(fill="x",padx=20,pady=(0,12))

        brand_lbl = customtkinter.CTkLabel(self.car_filter, text="Gyártmány / Márka:", anchor="w")
        brand_lbl.pack(fill="x", padx=20, pady=(5, 2))
        self.vehiclebrand_dropdown = customtkinter.CTkOptionMenu(self.car_filter,values=["Márka"], height=35)
        self.vehiclebrand_dropdown.pack(fill="x", padx=20, pady=(0,12))

        model_lbl = customtkinter.CTkLabel(self.car_filter, text="Modell:", anchor="w")
        model_lbl.pack(fill="x", padx=20, pady=(5, 2))
        self.model_dropdown = customtkinter.CTkOptionMenu(self.car_filter,values=["Modell"], height=35)
        self.model_dropdown.pack(fill="x", pady=(0,12), padx=20)

        engine_lbl = customtkinter.CTkLabel(self.car_filter, text="Motorkód:", anchor="w")
        engine_lbl.pack(fill="x", padx=20, pady=(5, 2))
        self.engine_dropdown = customtkinter.CTkOptionMenu(self.car_filter,values=["Motor"], height=35)
        self.engine_dropdown.pack(fill="x",pady=(0,20),padx=20)

        self.show_parts = customtkinter.CTkFrame(self, corner_radius=10)
        self.show_parts.grid(row=0, column=1, padx=(5, 15), pady=15, sticky="nsew")
        self.show_parts.grid_rowconfigure(1, weight=1)
        self.show_parts.grid_columnconfigure(0, weight=1)

        self.show_parts_label = customtkinter.CTkLabel(self.show_parts, text="Alkatrészek/Kompatibilitás hozzárendelés", font=(customtkinter.CTkFont(size=18, weight="bold")))
        self.show_parts_label.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="gray20", foreground="white", rowheight=26, fieldbackground="gray20", borderwidth=0)
        style.map('Treeview', background=[('selected', 'blue')])
        style.configure("Treeview.Heading", background="gray30", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', 'gray40')])
        self.parts_tree = ttk.Treeview(self.show_parts, selectmode="extended", columns=("Name","Manufacturer", "Type","Price"), show="headings", style="Treeview")
        self.parts_tree.heading("Name", text="Alkatrész")
        self.parts_tree.heading("Manufacturer", text="Gyártó")
        self.parts_tree.heading("Type", text="Típus / Kategória")
        self.parts_tree.heading("Price", text="Ár")

        self.parts_tree.column("Name", width=250, anchor="w")
        self.parts_tree.column("Manufacturer", width=140, anchor="center")
        self.parts_tree.column("Type", width=140, anchor="center")
        self.parts_tree.column("Price", width=100, anchor="e")
        self.parts_tree.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")

        action_frame = customtkinter.CTkFrame(self.show_parts, fg_color="transparent")
        action_frame.grid(row=2, column=0, padx=15, pady=15, sticky="ew")

        self.save_button = customtkinter.CTkButton(action_frame, text="Kijelöltek Hozzárendelése", command=self.save_action,fg_color="green",
                                                   hover_color="darkgreen", height=38, font=customtkinter.CTkFont(weight="bold"))
        self.save_button.grid(row=0, column=0, padx=(0, 10))
        self.delete_button = customtkinter.CTkButton(action_frame, text="Hozzárendelés Törlése", fg_color="red",hover_color="darkred", height=38, command=self.delete_action,
                                                     font=customtkinter.CTkFont(weight="bold"))
        self.delete_button.grid(row=0, column=1, padx=(0, 10))
        self.save_button_label = customtkinter.CTkLabel(action_frame, text="")
        self.save_button_label.grid(row=0, column=2, padx=5)
        self.reset_parts_button = customtkinter.CTkButton(action_frame, text="Összes alkatrész",command=lambda: self.controller.load_all_parts(),fg_color="gray40", hover_color="gray30", height=38)
        self.reset_parts_button.grid(row=0, column=3, padx=10)
        self.search_button = customtkinter.CTkButton(action_frame, text="Search", command=self.search_action)
        self.search_button.grid(row=0, column=4, padx=10)
        self.search_button_label = customtkinter.CTkLabel(action_frame, text="")
        self.search_button_label.grid(row=0, column=5, padx=5)