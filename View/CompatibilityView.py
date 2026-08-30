from tkinter import ttk, messagebox
import customtkinter

class CompatibilityView(customtkinter.CTkFrame):
    def search_action(self):
        self.selected_engine = self.engine_dropdown.get()
        self.controller.gets_parts_by_engine(self.selected_engine)

    def show_no_part_msgb(self):
        messagebox.showinfo("NoParts", "No parts for the engine")

    def __init__(self, master):
        super().__init__(master)


        self.car_filter = customtkinter.CTkFrame(self)
        self.car_filter.pack(fill="both",side="left", expand=True)
        self.car_filter_label = customtkinter.CTkLabel(self.car_filter, text="Filter")
        self.car_filter_label.pack(anchor="nw",padx=350, pady=(20,10))
        self.vehiclebrand_dropdown = customtkinter.CTkOptionMenu(self.car_filter,values=["Márka"])
        self.vehiclebrand_dropdown.pack(fill="x", pady=20, padx=20)
        self.model_dropdown = customtkinter.CTkOptionMenu(self.car_filter,values=["Modell"])
        self.model_dropdown.pack(fill="x", pady=20,padx=20)
        self.engine_dropdown = customtkinter.CTkOptionMenu(self.car_filter,values=["Motor"])
        self.engine_dropdown.pack(fill="x", pady=20,padx=20)

        self.show_parts = customtkinter.CTkFrame(self)
        self.show_parts_label = customtkinter.CTkLabel(self.show_parts, text="Parts")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="gray20", foreground="white", rowheight=25, fieldbackground="gray20",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', 'blue')])
        style.configure("Treeview.Heading", background="gray30", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', 'gray40')])
        self.parts_tree = ttk.Treeview(self.show_parts, selectmode="extended", columns=("Name","Brand", "Model","Engine"), show="headings", style="Treeview")
        self.parts_tree.heading("Name", text="Name")
        self.parts_tree.heading("Brand", text="Brand")
        self.parts_tree.heading("Model", text="Models")
        self.parts_tree.heading("Engine", text="Engines")
        self.parts_tree.pack(fill="both", expand=True)
        self.save_button = customtkinter.CTkButton(master=self.show_parts, text="Save")
        self.save_button.pack(side="left", padx=20, pady=20)
        self.save_button_label = customtkinter.CTkLabel(self.show_parts, text="")
        self.save_button_label.pack(side="left", padx=20, pady=20)
        self.search_button = customtkinter.CTkButton(master=self.show_parts, text="Search", command=self.search_action)
        self.search_button.pack(side="left", padx=20, pady=20)
        self.search_button_label = customtkinter.CTkLabel(self.show_parts, text="")
        self.search_button_label.pack(side="left", padx=20, pady=20)
        self.show_parts.pack(fill="both",side="right", expand=True)

