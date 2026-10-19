import datetime
from tkinter import messagebox, filedialog
from View.CartView import CartView
import customtkinter
from fpdf import FPDF
from sqlalchemy import func

from Model.database import Sessionlocal, Parts, TransactionLog, SellHeader, SellItem, User


class TransactionController:
    def __init__(self, main_app,view):
        self.main_app = main_app
        self.view = view
        self.cart = []
        self.load_all_parts()
        self.view.to_cart_save_button.configure(command=self.add_to_cart)
        self.view.search_bar.bind("<KeyRelease>", self.load_all_parts)
        self.view.cart_review_button.configure(command=self.show_cart)

    def load_all_parts(self, event=None):
        for item in self.view.transaction_tree.get_children():
            self.view.transaction_tree.delete(item)

        with Sessionlocal() as session:
            try:
                search_term = self.view.search_bar.get()
                if search_term:
                    all_parts=session.query(Parts).filter(Parts.name.ilike(f"%{search_term}%")).all()
                else:
                    all_parts = session.query(Parts).all()

                for part in all_parts:
                        self.view.transaction_tree.insert("", "end", values=(part.id, part.name, part.amount))
            except Exception as e:
                print("Hiba történt az adatbázis mentésekor!",e)

    def load_transaction_history(self):
        if not hasattr(self.view, 'history_tree'):
            return

        for item in self.view.history_tree.get_children():
            self.view.history_tree.delete(item)

        with Sessionlocal() as session:
            try:
                logs = (
                    session.query(TransactionLog, Parts.name, User.name)
                    .join(Parts, TransactionLog.part_id == Parts.id)
                    .join(User, TransactionLog.user_id == User.id)
                    .order_by(TransactionLog.date.desc())
                    .limit(50)
                    .all()
                )
                for log, part_name, user_name in logs:
                    if log.date:
                        formatted_date = log.date.strftime("%Y-%m-%d %H:%M")
                    else:
                        formatted_date = "-"
                    if log.quantity > 0:
                        qty_str = f"+{log.quantity}"
                    else:
                        qty_str = str(log.quantity)
                    self.view.history_tree.insert(
                        "", "end", values=(log.id, formatted_date, log.transaction_type, part_name, qty_str, user_name)
                    )
            except Exception as e:
                print("Hiba a tranzakciós napló betöltésekor:", e)

    def add_to_cart(self):
        chosed_line = self.view.transaction_tree.selection()

        if not chosed_line:
            messagebox.showerror("Hiba", "Kérlek válassz ki egy alkatrészt!")
            return

        raw_quantity = self.view.transaction_quantity_menu.get()

        if not raw_quantity:
            messagebox.showerror("Hiba", "Kérlek érvényes számot adj meg!")
            return

        line_datas = self.view.transaction_tree.item(chosed_line[0])["values"]
        part_id = line_datas[0]
        part_name = line_datas[1]
        current_stock = int(line_datas[2])

        ptr_type = self.view.transaction_type_menu.get()
        if len(self.cart) > 0:
            current_cart_type = self.cart[0]["type"]
            if ptr_type != current_cart_type:
                messagebox.showerror("Hiba", f"A kosaradban már {current_cart_type} típusú tételek vannak!")
                return

        ptr_quantity = int(raw_quantity)
        if ptr_type == "Kiadás" and ptr_quantity > current_stock:
            messagebox.showerror("Hiba", f"Nincs elegendő készlet! (Elérhető: {current_stock} db)")
            return

        with Sessionlocal() as session:
            part = session.query(Parts).filter(Parts.id == part_id).first()
            if part and part.price:
                price = part.price
            else:
                price = 0

            cart_item = {
                "part_id": part_id,
                "name": part_name,
                "type": ptr_type,
                "quantity": ptr_quantity,
                "price": price,
                "total": price * ptr_quantity
            }

            self.cart.append(cart_item)
            self.load_transaction_history()

        messagebox.showinfo("Siker", f"{part_name} ({ptr_quantity} db) került be a kosárba!")
        self.view.transaction_quantity_menu.delete(0,"end")

    def show_cart(self):
        if not self.cart:
            messagebox.showwarning("Üres kosár", "A kosarad jelenleg üres!")
            return

        CartView(self.view, self.cart, self.execute_cart_transaction)

    def execute_cart_transaction(self):
        if not self.cart:
            return False

        cart_type = self.cart[0]["type"]
        buyer_name = "-"

        if cart_type == "Kiadás":
            dialog = customtkinter.CTkInputDialog(text='Kérlek add meg a vevő nevét: ', title="Vevő neve")
            buyer_name = dialog.get_input()
            if not buyer_name:
                return False

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Szállítólevél mentése"
        )
        if not filepath:
            return False

        with Sessionlocal() as session:
            user_id = self.main_app.current_user.id if self.main_app.current_user else 1

            max_num = session.query(func.max(SellHeader.number)).scalar() or 10000
            new_header = SellHeader(date=datetime.datetime.now(), number=max_num + 1)
            session.add(new_header)
            session.flush()

            for item in self.cart:
                current_part = session.query(Parts).filter(Parts.id == item["part_id"]).first()

                if cart_type == "Bevételezés":
                    current_part.amount += item["quantity"]
                    log_qty = item["quantity"]
                    log_type = "Bevételezés"
                else:
                    current_part.amount -= item["quantity"]
                    log_qty = -item["quantity"]
                    log_type = "Eladás"

                new_item = SellItem(
                    sell_header_id=new_header.id,
                    part_id=current_part.id,
                    amount=item["quantity"],
                    price=current_part.price
                )
                session.add(new_item)

                new_transaction = TransactionLog(
                    transaction_type=log_type,
                    user_id=user_id,
                    quantity=log_qty,
                    part_id=item["part_id"],
                    date=datetime.datetime.now()
                )
                session.add(new_transaction)
            session.commit()

        self.generate_batch_receipt(filepath, buyer_name, cart_type)

        messagebox.showinfo("Siker", f"A tranzakció sikeresen rögzítve, PDF legenerálva!")
        self.cart.clear()
        self.load_all_parts()
        self.load_transaction_history()
        return True
    def generate_batch_receipt(self, filepath, buyer_name, cart_type):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("Arial", "", "assets/fonts/arial.ttf")
            pdf.add_font("Arial", "B", "assets/fonts/arialbd.ttf")
            pdf.add_font("Arial", "I", "assets/fonts/ariali.ttf")

            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, text="Szállítólevél", new_x="LMARGIN", new_y="NEXT", align="center")
            pdf.ln(10)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, text=f"Dátum: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN",
                     new_y="NEXT", align="center")
            pdf.cell(0, 8, text=f"Tranzakció típusa: {cart_type}", new_x="LMARGIN", new_y="NEXT", align="center")
            if cart_type == "Kiadás":
                pdf.cell(0, 8, text=f"Vevő neve: {buyer_name}", new_x="LMARGIN", new_y="NEXT", align="center")
            pdf.ln(10)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(90, 10, "Megnevezés", border=1, align="L")
            pdf.cell(30, 10, "Mennyiség", border=1, align="C")
            pdf.cell(35, 10, "Egységár", border=1, align="R")
            pdf.cell(35, 10, "Összesen", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

            pdf.set_font("Arial", "", 12)
            grand_total = 0
            for item in self.cart:
                safe_name = item["name"][:40]
                pdf.cell(90, 10, safe_name, border=1, align="L")
                pdf.cell(30, 10, f"{item['quantity']} db", border=1, align="C")
                pdf.cell(35, 10, f"{item['price']} Ft", border=1, align="R")
                pdf.cell(35, 10, f"{item['total']} Ft", border=1, align="R", new_x="LMARGIN", new_y="NEXT")
                grand_total += item["total"]

            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(155, 10, "Végösszeg:", align="R")
            pdf.cell(35, 10, f"{grand_total} Ft", align="R", new_x="LMARGIN", new_y="NEXT")

            pdf.ln(20)
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 10, "Köszönjük!", align="center")

            pdf.output(filepath)
        except Exception as e:
            print(f"Hiba a pdf generálásakor: {e}")

    def valid_quantity(self, raw_quantity):
        if not raw_quantity.isdigit() or int(raw_quantity) <= 0:
            return False
        return True