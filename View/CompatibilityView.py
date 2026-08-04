from tkinter import ttk

import customtkinter

class CompatibilityView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


        self.car_filter = customtkinter.CTkFrame(self)
        self.car_filter.pack(fill="both",side="left", expand=True)
        self.car_filter_label = customtkinter.CTkLabel(self.car_filter, text="Filter")
        self.car_filter_label.pack(anchor="nw",padx=350, pady=(20,10))
        self.manufacturer_dropdown = customtkinter.CTkOptionMenu(self.car_filter,values=["Ford"])
        self.manufacturer_dropdown.pack(fill="x", pady=20, padx=20)
        self.model_dropdown = customtkinter.CTkOptionMenu(self.car_filter,values=["Mustang"])
        self.model_dropdown.pack(fill="x", pady=20,padx=20)
        self.engine_dropdown = customtkinter.CTkOptionMenu(self.car_filter,values=["500"])
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
        self.parts_tree = ttk.Treeview(self.show_parts, selectmode="extended", columns=("Name","Manufacturer", "Model","Engine"), show="headings", style="Treeview")
        self.parts_tree.heading("Name", text="Name")
        self.parts_tree.heading("Manufacturer", text="Manufacturers")
        self.parts_tree.heading("Model", text="Models")
        self.parts_tree.heading("Engine", text="Engines")
        self.parts_tree.pack(fill="both", expand=True)
        self.save_button = customtkinter.CTkButton(master=self.show_parts, text="Save")
        self.save_button.pack(side="left", padx=20, pady=20)
        self.save_button_label = customtkinter.CTkLabel(self.show_parts, text="")
        self.save_button_label.pack(side="left", padx=20, pady=20)
        self.show_parts.pack(fill="both",side="right", expand=True)

