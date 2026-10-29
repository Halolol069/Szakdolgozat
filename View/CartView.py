import customtkinter
from tkinter import ttk, messagebox


class CartView(customtkinter.CTkToplevel):
    def __init__(self, master, cart, checkout_callback):
        super().__init__(master)
        self.title("Kosár megtekintése")
        self.geometry("680x550")
        self.cart = cart
        self.checkout_callback = checkout_callback

        self.grab_set()

        self.title_label = customtkinter.CTkLabel(self, text="Kosár tartalma", font=customtkinter.CTkFont(size=22, weight="bold"))
        self.title_label.pack(pady=(20,10))

        table_frame = customtkinter.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="gray20", foreground="white", rowheight=28, fieldbackground="gray20", borderwidth=0)
        style.map("Treeview", background=[("selected", "#1f538d")])
        style.configure("Treeview.Heading", background="gray30", foreground="white", relief="flat")

        columns = ("name", "quantity", "price", "total")
        self.cart_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10, style="Treeview")
        self.cart_tree.heading("name", text="Alkatrész neve")
        self.cart_tree.heading("quantity", text="Mennyiség")
        self.cart_tree.heading("price", text="Ár (Ft)")
        self.cart_tree.heading("total", text="Összesen (Ft)")

        self.cart_tree.column("name", width=280, anchor="w")
        self.cart_tree.column("quantity", width=100, anchor="center")
        self.cart_tree.column("price", width=120, anchor="e")
        self.cart_tree.column("total", width=130, anchor="e")
        self.cart_tree.pack(fill="both", expand=True, padx=10, pady=10)

        summary_frame = customtkinter.CTkFrame(self, fg_color="gray25", corner_radius=8)
        summary_frame.pack(fill="x", padx=20, pady=5)

        self.total_label = customtkinter.CTkLabel(self, text="Végösszeg: 0 Ft", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.total_label.pack(pady=10, anchor="e", padx=20)

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=15, fill="x", padx=20)

        self.checkout_button = customtkinter.CTkButton(self.button_frame, text="Fizetés és Szállítólevél nyomtatása",
                                                       command=self.do_checkout, fg_color="green", hover_color="darkgreen", height=40, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.checkout_button.pack(side="left",padx=(0,10), expand=True, fill='x')

        self.delete_button = customtkinter.CTkButton(self.button_frame, text="Törlés", command=self.delete_part, height=40, width=130)
        self.delete_button.pack(side="left", padx=10)

        self.cancel_button = customtkinter.CTkButton(self.button_frame, text="Mégsem", command=self.destroy, fg_color="red", hover_color="darkred", height=40, width=110)
        self.cancel_button.pack(side="right",padx=(10,0))

        self.load_cart_data()

    def load_cart_data(self):
        grand_total = 0
        for item in self.cart:
            self.cart_tree.insert("","end", values=(
                item["name"],
                item["quantity"],
                f"{item['price']} Ft",
                f"{item['total']} Ft"
            ))
            grand_total += item['total']

        self.total_label.configure(text=f"Végösszeg: {grand_total} Ft")

    def do_checkout(self):
        success = self.checkout_callback()
        if success:
            self.destroy()


    def delete_part(self):
        selected_part = self.cart_tree.selection()

        if not selected_part:
            messagebox.showerror("Hiba", "Nincs kijelölt alkatrész!")
            return

        item_id = selected_part[0]
        item_index = self.cart_tree.index(item_id)

        self.cart.pop(item_index)
        self.cart_tree.delete(item_id)

        grand_total = 0
        for item in self.cart:
            grand_total += item['total']
        self.total_label.configure(text=f"Végösszeg: {grand_total} Ft")

        if len(self.cart) == 0:
            messagebox.showerror("Kosár", "A kosár kiürült!")
            self.destroy()