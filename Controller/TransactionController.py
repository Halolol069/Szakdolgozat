import datetime
import os
from tkinter import messagebox, filedialog

import customtkinter
from fpdf import FPDF

from Model.database import Sessionlocal, Parts, TransactionLog


class TransactionController:
    def __init__(self, main_app,view):
        self.main_app = main_app
        self.view = view
        self.load_all_parts()
        self.view.save_button.configure(command=self.execute_transaction)
        self.view.search_bar.bind("<KeyRelease>", self.load_all_parts)
        self.view.receipt_button.configure(command=self.generate_receipt)

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

    def save_transaction_log(self, transaction_type, quantity, part_id):
        with Sessionlocal() as session:
            new_transaction = TransactionLog(transaction_type=transaction_type, user_id=self.main_app.current_user.id,
                                             quantity=quantity, part_id=part_id)
            current_part = session.query(Parts).filter(Parts.id == part_id).first()
            if transaction_type == "Bevételezés":
                current_part.amount += quantity
            elif transaction_type == "Kiadás":
                current_part.amount -= quantity
            session.add(new_transaction)
            session.commit()

    def valid_quantity(self, raw_quantity):
        if not raw_quantity.isdigit() or int(raw_quantity) <= 0:
            return False
        return True

    def execute_transaction(self):
        chosed_line = self.view.transaction_tree.selection()

        if not chosed_line:
            messagebox.showerror("Hiba", "Kérlek válassz ki egy alkatrészt!")
            return

        raw_quantity = self.view.transaction_quantity_menu.get()

        if not self.valid_quantity(raw_quantity):
            messagebox.showerror("Hiba", "Kérlek érvényes számot adj meg a mennyiséghez!")
            return
        line_datas = self.view.transaction_tree.item(chosed_line[0])["values"]
        chosed_line_id = line_datas[0]
        ptr_type = self.view.transaction_type_menu.get()
        ptr_quantity = int(raw_quantity)
        if ptr_type == "Kiadás" and ptr_quantity > line_datas[2]:
            messagebox.showerror("Hiba", "Nem megfelelő mennyiség!")
            return
        self.save_transaction_log(ptr_type, ptr_quantity, chosed_line_id)
        self.load_all_parts()

    def generate_receipt(self):
        chosed_line = self.view.transaction_tree.selection()

        if not chosed_line:
            messagebox.showerror("Hiba", "Kérlek válasz ki egy alkatrészt a bizonylathoz!")
            return

        raw_quantity = self.view.transaction_quantity_menu.get()

        if not self.valid_quantity(raw_quantity):
            messagebox.showerror("Hiba", "Kérlek adj meg érvényes számot a mennyiséghez")
            return

        dialog = customtkinter.CTkInputDialog(text='Kérlek add meg a vevő nevét: ', title="Vevő neve")
        buyer_name = dialog.get_input()

        if not buyer_name:
            return

        line_datas = self.view.transaction_tree.item(chosed_line[0])["values"]
        part_id = line_datas[0]
        part_name = line_datas[1]
        quantity = int(raw_quantity)

        with Sessionlocal() as session:
            part = session.query(Parts).filter(Parts.id == part_id).first()
            if part.price:
                price = part.price
            else:
                price = 0
            total_price = price * quantity
            part_image_path = part.image_path

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Szállítólevél mentése"
        )

        if not filepath:
            return

        try:
            pdf = FPDF()
            pdf.add_page()

            pdf.add_font("Arial","", "assets/fonts/arial.ttf")
            pdf.add_font("Arial","B", "assets/fonts/arialbd.ttf")
            pdf.add_font("Arial", "I", "assets/fonts/ariali.ttf")

            pdf.set_font("Arial", "B",16)
            pdf.cell(0,10, text="Szállítólevél", new_x="LMARGIN", new_y="NEXT", align="center")
            pdf.ln(10)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0,8, text=f"Dátum: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT", align="center")
            pdf.cell(0,8,text=f"Vevő neve: {buyer_name}", new_x="LMARGIN", new_y="NEXT", align="center")
            pdf.ln(10)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(90,10,"Megnevezés", border=1, align="L")
            pdf.cell(30,10, "Mennyiség", border=1, align="L")
            pdf.cell(35,10, "Egységár", border=1, align="R")
            pdf.cell(35,10, "Összesen", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

            pdf.set_font("Arial", "B", 12)
            safe_name = part_name[:40]
            pdf.cell(90,10, safe_name, border=1, align="L")
            pdf.cell(30,10, f"{quantity} db", border=1, align="center")
            pdf.cell(35,10, f"{price} Ft", border=1, align="R")
            pdf.cell(35,10, f"{total_price} Ft", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

            if part_image_path and os.path.exists(part_image_path):
                pdf.ln(10)
                pdf.set_font("Arial", "B", 10)
                pdf.cell(0,10,"A megvásárolt alkatrész: ", new_x="LMARGIN", new_y="NEXT", align="C")

                pdf.image(part_image_path, x=85, y=pdf.get_y(), w=40)
                pdf.ln(45)
            else:
                pdf.ln(20)

            pdf.set_font("Arial", "I", 10)
            pdf.cell(0,10, "Köszönjük a vásárlást!", align="center")

            pdf.output(filepath)
            messagebox.showinfo("Siker", f"A szállítólevél sikeresen elmentve!")
        except Exception as e:
            print(f"Hiba a pdf generálásakor: {e}")
            messagebox.showerror("Hiba", "Nem sikerült legenerálni a PDF-et.")

