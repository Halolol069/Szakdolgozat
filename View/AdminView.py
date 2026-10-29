from tkinter import ttk
import customtkinter


class AdminView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.user_tab = self.tabview.add("Felhasználókezelés")
        self.log_tab = self.tabview.add("Tranzakciók és Stornó")
        self.catalog_tab = self.tabview.add("Katalógus (Gyártók / Márkák)")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="gray20", foreground="white", rowheight=25, fieldbackground="gray20",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', 'blue')])
        style.configure("Treeview.Heading", background="gray30", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', 'gray40')])

        self.build_user_tab()
        self.build_log_tab()
        self.build_catalog_tab()

    def build_user_tab(self):
        self.user_tab.grid_columnconfigure((0, 1, 2), weight=1)
        self.user_tab.grid_rowconfigure(0, weight=1)

        self.user_tree = ttk.Treeview(
            self.user_tab, selectmode="browse",
            columns=("ID", "Name", "Email", "Phone", "Role", "Status"),
            show="headings", style="Treeview"
        )
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Name", text="Név")
        self.user_tree.heading("Email", text="E-mail")
        self.user_tree.heading("Phone", text="Telefon")
        self.user_tree.heading("Role", text="Szerepkör")
        self.user_tree.heading("Status", text="Állapot")

        self.user_tree.column("ID", width=50, anchor="center")
        self.user_tree.column("Name", width=150, anchor="w")
        self.user_tree.column("Email", width=200, anchor="w")
        self.user_tree.column("Phone", width=130, anchor="center")
        self.user_tree.column("Role", width=100, anchor="center")
        self.user_tree.column("Status", width=100, anchor="center")
        self.user_tree.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.toggle_status_btn = customtkinter.CTkButton(
            self.user_tab, text="Fiók Felfüggesztése / Aktiválása", fg_color="#d97706", hover_color="#b45309"
        )
        self.toggle_status_btn.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.reset_pw_btn = customtkinter.CTkButton(
            self.user_tab, text="Jelszó visszaállítása"
        )
        self.reset_pw_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.change_role_btn = customtkinter.CTkButton(
            self.user_tab, text="Szerepkör váltása (Admin <-> Raktáros)", fg_color="gray40", hover_color="gray30"
        )
        self.change_role_btn.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        form_frame = customtkinter.CTkFrame(self.user_tab)
        form_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        form_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.new_user_name = customtkinter.CTkEntry(form_frame, placeholder_text="Felhasználónév")
        self.new_user_name.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        self.new_user_email = customtkinter.CTkEntry(form_frame, placeholder_text="E-mail cím")
        self.new_user_email.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.new_user_phone = customtkinter.CTkEntry(form_frame, placeholder_text="Telefonszám")
        self.new_user_phone.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

        self.new_user_pw = customtkinter.CTkEntry(form_frame, placeholder_text="Jelszó", show="*")
        self.new_user_pw.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

        self.new_user_role = customtkinter.CTkOptionMenu(form_frame, values=["Raktaros", "Admin"])
        self.new_user_role.grid(row=0, column=4, padx=5, pady=10, sticky="ew")

        self.add_user_btn = customtkinter.CTkButton(
            form_frame, text="Új felhasználó felvétele", fg_color="green", hover_color="darkgreen"
        )
        self.add_user_btn.grid(row=0, column=5, padx=5, pady=10, sticky="ew")

    def build_log_tab(self):
        self.log_tab.grid_columnconfigure(0, weight=1)
        self.log_tab.grid_rowconfigure(1, weight=1)

        top_frame = customtkinter.CTkFrame(self.log_tab, fg_color="transparent")
        top_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)

        self.log_search_entry = customtkinter.CTkEntry(
            top_frame, placeholder_text="Szűrés alkatrészre, felhasználóra vagy műveletre..."
        )
        self.log_search_entry.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")

        self.storno_btn = customtkinter.CTkButton(
            top_frame, text="Kijelölt tranzakció STORNÓZÁSA (Készlet visszaállítása)",
            fg_color="#dc2626", hover_color="#991b1b"
        )
        self.storno_btn.grid(row=0, column=1, padx=5, pady=5)

        self.admin_log_tree = ttk.Treeview(
            self.log_tab, selectmode="browse",
            columns=("ID", "Date", "Type", "Part", "Qty", "User"),
            show="headings", style="Treeview"
        )
        self.admin_log_tree.heading("ID", text="Napló ID")
        self.admin_log_tree.heading("Date", text="Dátum")
        self.admin_log_tree.heading("Type", text="Művelet típusa")
        self.admin_log_tree.heading("Part", text="Alkatrész")
        self.admin_log_tree.heading("Qty", text="Mennyiség változás")
        self.admin_log_tree.heading("User", text="Elkövető (Felhasználó)")

        self.admin_log_tree.column("ID", width=70, anchor="center")
        self.admin_log_tree.column("Date", width=150, anchor="center")
        self.admin_log_tree.column("Type", width=140, anchor="center")
        self.admin_log_tree.column("Part", width=280, anchor="w")
        self.admin_log_tree.column("Qty", width=120, anchor="center")
        self.admin_log_tree.column("User", width=150, anchor="center")
        self.admin_log_tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def build_catalog_tab(self):
        self.catalog_tab.grid_columnconfigure((0, 1), weight=1)
        self.catalog_tab.grid_rowconfigure(1, weight=1)

        man_label = customtkinter.CTkLabel(self.catalog_tab, text="Alkatrészgyártók", font=("Arial", 16, "bold"))
        man_label.grid(row=0, column=0, padx=10, pady=5)

        self.man_tree = ttk.Treeview(
            self.catalog_tab, selectmode="browse", columns=("ID", "Name"), show="headings", style="Treeview"
        )
        self.man_tree.heading("ID", text="ID")
        self.man_tree.heading("Name", text="Gyártó neve")
        self.man_tree.column("ID", width=60, anchor="center")
        self.man_tree.column("Name", width=250, anchor="w")
        self.man_tree.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        man_form = customtkinter.CTkFrame(self.catalog_tab)
        man_form.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        man_form.grid_columnconfigure(0, weight=1)

        self.man_name_entry = customtkinter.CTkEntry(man_form, placeholder_text="Gyártó neve (pl. Brembo)")
        self.man_name_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.add_man_btn = customtkinter.CTkButton(man_form, text="Hozzáadás", width=100)
        self.add_man_btn.grid(row=0, column=1, padx=5, pady=5)

        self.rename_man_btn = customtkinter.CTkButton(
            man_form, text="Kijelölt átnevezése", width=140, fg_color="gray40", hover_color="gray30"
        )
        self.rename_man_btn.grid(row=0, column=2, padx=5, pady=5)

        brand_label = customtkinter.CTkLabel(self.catalog_tab, text="Járműmárkák", font=("Arial", 16, "bold"))
        brand_label.grid(row=0, column=1, padx=10, pady=5)

        self.brand_tree = ttk.Treeview(
            self.catalog_tab, selectmode="browse", columns=("ID", "Name", "Country"), show="headings", style="Treeview"
        )
        self.brand_tree.heading("ID", text="ID")
        self.brand_tree.heading("Name", text="Márka neve")
        self.brand_tree.heading("Country", text="Származási ország")
        self.brand_tree.column("ID", width=60, anchor="center")
        self.brand_tree.column("Name", width=180, anchor="w")
        self.brand_tree.column("Country", width=150, anchor="center")
        self.brand_tree.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        brand_form = customtkinter.CTkFrame(self.catalog_tab)
        brand_form.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        brand_form.grid_columnconfigure((0, 1), weight=1)

        self.brand_name_entry = customtkinter.CTkEntry(brand_form, placeholder_text="Márka (pl. Audi)")
        self.brand_name_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.brand_country_entry = customtkinter.CTkEntry(brand_form, placeholder_text="Ország (pl. Germany)")
        self.brand_country_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.add_brand_btn = customtkinter.CTkButton(brand_form, text="Hozzáadás", width=100)
        self.add_brand_btn.grid(row=0, column=2, padx=5, pady=5)

        self.update_brand_btn = customtkinter.CTkButton(
            brand_form, text="Módosítás", width=100, fg_color="gray40", hover_color="gray30"
        )
        self.update_brand_btn.grid(row=0, column=3, padx=5, pady=5)