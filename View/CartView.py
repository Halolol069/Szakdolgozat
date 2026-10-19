import customtkinter
from tkinter import ttk, messagebox


class CartView(customtkinter.CTkToplevel):
    def __init__(self, master, cart, checkout_callback):
        super().__init__(master)
        self.title("Kosár megtekintése")
        self.geometry("600x600")
        self.cart = cart
        self.checkout_callback = checkout_callback

        self.grab_set()

        self.title_label = customtkinter.CTkLabel(self, text="Kosár tartalma", font=('Arial', 20, 'bold'))
        self.title_label.pack(pady=10)

        columns = ("name", "quantity", "price", "total")
        self.cart_tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.cart_tree.heading("name", text="Alkatrész neve")
        self.cart_tree.heading("quantity", text="Mennyiség")
        self.cart_tree.heading("price", text="Ár (Ft)")
        self.cart_tree.heading("total", text="Összesen (Ft)")

        self.cart_tree.column("name", width=250)
        self.cart_tree.column("quantity", width=80, anchor="center")
        self.cart_tree.column("price", width=100, anchor="e")
        self.cart_tree.column("total", width=120, anchor="e")

        self.cart_tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.total_label = customtkinter.CTkLabel(self, text="Végösszeg: 0 Ft", font=('Arial', 18, 'bold'))
        self.total_label.pack(pady=5, anchor="e", padx=20)

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=15)

        self.checkout_button = customtkinter.CTkButton(self.button_frame, text="Fizetés és Szállítólevél nyomtatása",
                                                       command=self.do_checkout, fg_color="green", hover_color="darkgreen")
        self.checkout_button.pack(side="left",padx=10)

        self.delete_button = customtkinter.CTkButton(self.button_frame, text="Törlés", command=self.delete_part)
        self.delete_button.pack(side="left", padx=15)

        self.cancel_button = customtkinter.CTkButton(self.button_frame, text="Mégsem", command=self.destroy, fg_color="red", hover_color="darkred")
        self.cancel_button.pack(side="right",padx=10)

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