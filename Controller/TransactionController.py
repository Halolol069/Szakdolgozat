import datetime
import os
from tkinter import messagebox, filedialog
import qrcode
from View.CartView import CartView
import customtkinter
from fpdf import FPDF
from sqlalchemy import func, text
from pathlib import Path
from Model.database import Sessionlocal, Parts, TransactionLog, SellHeader, SellItem, User, VehicleBrand, Modell, \
    Compatibility, Engine, VehicleType, Vehicle
from Controller.permissions import require_active_user
from Controller.model_labels import build_model_labels, resolve_model_id

FONT_DIR = Path(__file__).resolve().parent / "assets" / "fonts"
def next_receipt_number(session):
    if session.get_bind().dialect.name == "postgresql":
        return session.execute(text("SELECT nextval('sell_header_number_seq')")).scalar()
    return (session.query(func.max(SellHeader.number)).scalar() or 10000) + 1

class TransactionController:
    def __init__(self, main_app,view):
        self.main_app = main_app
        self.view = view
        self.cart = []
        self.model_map = {}
        self.load_all_parts()
        self.view.to_cart_save_button.configure(command=self.add_to_cart)
        self.view.search_bar.bind("<KeyRelease>", self.load_all_parts)
        self.view.cart_review_button.configure(command=self.show_cart)

        if hasattr(self.view, "reprint_button"):
            self.view.reprint_button.configure(command=self.reprint_receipt)

        if hasattr(self.view, "vehicletype_dropdown"):
            self.load_vehicle_types()
            self.view.reset_filter_button.configure(command=self.reset_filters)
        self.load_transaction_history()

    def load_vehicle_types(self):
        with Sessionlocal() as session:
            try:
                types = session.query(VehicleType).all()
                type_list = [t.name for t in types]
                self.view.vehicletype_dropdown.configure(values=type_list, command=self.load_brands)
                self.view.vehicletype_dropdown.set("Jármű típus")
            except Exception as e:
                print("Hiba a járműtípusok betöltésekor!", e)

    def load_brands(self, selected_type=None):
        self.view.brand_dropdown.configure(values=["Márka"])
        self.view.brand_dropdown.set("Márka")
        self.view.model_dropdown.configure(values=["Modell"])
        self.view.model_dropdown.set("Modell")
        self.view.engine_dropdown.configure(values=["Motor"])
        self.view.engine_dropdown.set("Motor")
        self.load_all_parts()
        if not selected_type or selected_type == "Jármű típus":
            return
        with Sessionlocal() as session:
            try:
                brands = (session.query(VehicleBrand)
                          .join(Modell, Modell.vehicleBrand_id == VehicleBrand.id)
                          .join(Vehicle,Vehicle.modell_id == Modell.id )
                          .join(VehicleType, Vehicle.vehicle_type_id == VehicleType.id)
                          .filter(VehicleType.name == selected_type).distinct()
                          .order_by(VehicleBrand.name)
                          .all())
                brand_list = [b.name for b in brands]
                self.view.brand_dropdown.configure(values=brand_list, command=self.load_model)
                self.view.brand_dropdown.set("Márka")
            except Exception as e:
                print("Hiba a márkák betöltésekor!", e)

    def load_model(self, selected_brand):
        self.view.model_dropdown.configure(values=["Modell"])
        self.view.model_dropdown.set("Modell")
        self.view.engine_dropdown.configure(values=["Motor"])
        self.view.engine_dropdown.set("Motor")
        self.load_all_parts()

        with Sessionlocal() as session:
            try:
                query = (
                    session.query(Modell)
                    .join(VehicleBrand)
                    .filter(VehicleBrand.name == selected_brand)
                )
                selected_type = self.view.vehicletype_dropdown.get() if hasattr(self.view,
                                                                                "vehicletype_dropdown") else None
                if selected_type and selected_type != "Jármű típus":
                    query = (query.join(Vehicle, Vehicle.modell_id == Modell.id)
                             .join(VehicleType, Vehicle.vehicle_type_id == VehicleType.id)
                             .filter(VehicleType.name == selected_type))
                models = query.distinct().all()
                model_list, self.model_map = build_model_labels(models)
                self.view.model_dropdown.configure(values=model_list, command=self.load_engines)
            except Exception as e:
                print("Hiba a modellek betöltésekor!", e)

    def load_engines(self, selected_model):
        self.view.engine_dropdown.configure(values=["Motor"])
        self.view.engine_dropdown.set("Motor")
        self.load_all_parts()

        with Sessionlocal() as session:
            try:
                model_id = resolve_model_id(session, selected_model, self.model_map)
                model = session.get(Modell, model_id) if model_id is not None else None
                engine_list = []
                if model:
                    for mc in model.motor_comps:
                        engine_list.append(f"[{mc.engine.id}] {mc.engine.engine_code} | {mc.engine.ccc}ccm, {mc.engine.horse_power}LE")

                self.view.engine_dropdown.configure(values=engine_list, command=self.filter_parts_by_vehicle)
            except Exception as e:
                print("Hiba a motorok betöltésekor!", e)

    def filter_parts_by_vehicle(self, selected_engine):
        self.load_all_parts(show_empty_message=True)

    def get_vehicle_filter(self, session):
        if not hasattr(self.view, "engine_dropdown"):
            return None
        raw_engine = self.view.engine_dropdown.get()
        if not raw_engine or not raw_engine.startswith("["):
            return None
        try:
            engine_id = int(raw_engine.split("]")[0].replace("[", ""))
        except ValueError:
            return None
        model_id = resolve_model_id(session, self.view.model_dropdown.get(), self.model_map)
        if model_id is None:
            return None
        return model_id, engine_id
    def reset_filters(self):
        if hasattr(self.view, "vehicletype_dropdown"):
            self.view.vehicletype_dropdown.set("Jármű típus")
        if hasattr(self.view, 'brand_dropdown'):
            self.view.brand_dropdown.set("Márka")
            self.view.model_dropdown.configure(values=["Modell"])
            self.view.model_dropdown.set("Modell")
            self.view.engine_dropdown.configure(values=["Motor"])
            self.view.engine_dropdown.set("Motor")
        self.view.search_bar.delete(0, "end")
        self.load_all_parts()

    def load_all_parts(self, event=None, show_empty_message=False):
        for item in self.view.transaction_tree.get_children():
            self.view.transaction_tree.delete(item)

        with Sessionlocal() as session:
            try:
                query = session.query(Parts)
                vehicle_filter = self.get_vehicle_filter(session)
                if vehicle_filter:
                    model_id, engine_id = vehicle_filter
                    query = (query.join(Compatibility, Parts.id == Compatibility.part_id)
                             .filter(Compatibility.modell_id == model_id, Compatibility.engine_id == engine_id))

                search_term = self.view.search_bar.get().strip()
                if search_term:
                    query = query.filter(Parts.name.ilike(f"%{search_term}%") |
                                         Parts.part_number.ilike(f"%{search_term}%") |
                                         Parts.type.ilike(f"%{search_term}%"))

                all_parts = query.order_by(Parts.id).all()

                if vehicle_filter and not all_parts and show_empty_message:
                    messagebox.showinfo("Nincs találat","Ehhez a járműhöz jelenleg nincs rögzített kompatibilis alkatrész!")

                for part in all_parts:
                    self.view.transaction_tree.insert("", "end", values=(part.id, part.part_number, part.name, part.amount,part.type, part.price, part.location))
            except Exception as e:
                print("Hiba történt az alkatrészek betöltésekor!", e)

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

        if not self.valid_quantity(raw_quantity):
            messagebox.showerror("Hiba", "Kérlek érvényes számot adj meg!")
            return

        line_datas = self.view.transaction_tree.item(chosed_line[0])["values"]
        part_id = line_datas[0]
        part_number = line_datas[1]
        part_name = line_datas[2]
        current_stock = int(line_datas[3])

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
                "part_number": part_number,
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

        user = self.main_app.current_user
        if user is None:
            messagebox.showerror("Hiba", "Nincs bejelentkezett felhasználó!")
            return False

        if not require_active_user(self.main_app):
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

        receipt_number = None
        with Sessionlocal() as session:
            try:
                new_header = None
                if cart_type == "Kiadás":
                    new_header = SellHeader(date=datetime.datetime.now(), number=next_receipt_number(session),buyer_name=buyer_name)
                    session.add(new_header)
                    session.flush()
                    receipt_number = new_header.number

                for item in self.cart:
                    current_part = session.query(Parts).filter(Parts.id == item["part_id"]).with_for_update().first()

                    if cart_type == "Bevételezés":
                        current_part.amount += item["quantity"]
                        log_qty = item["quantity"]
                        log_type = "Bevételezés"
                    else:
                        if current_part.amount < item["quantity"]:
                            session.rollback()
                            messagebox.showerror("Hiba", f"Nincs elegendő készlet ebből: {current_part.name}!")
                            return False

                        current_part.amount -= item["quantity"]
                        log_qty = -item["quantity"]
                        log_type = f"Eladás (Vevő: {buyer_name})"

                        new_item = SellItem(
                            sell_header_id=new_header.id,
                            part_id=current_part.id,
                            amount=item["quantity"],
                            price=item["price"]
                        )
                        session.add(new_item)

                    new_transaction = TransactionLog(
                        transaction_type=log_type,
                        user_id=user.id,
                        quantity=log_qty,
                        part_id=item["part_id"],
                        date=datetime.datetime.now()
                    )
                    session.add(new_transaction)

                session.commit()
            except Exception as e:
                session.rollback()
                print("Adatbázis hiba a tranzakció során:", e)
                messagebox.showerror("Hiba", "Váratlan hiba történt a mentéskor!")
                return False

        if self.generate_batch_receipt(filepath, buyer_name, cart_type, receipt_number=receipt_number):
            messagebox.showinfo("Siker", "A tranzakció sikeresen rögzítve, PDF legenerálva!")
        elif receipt_number is not None:
            messagebox.showwarning("Figyelem",f"A tranzakció rögzítve lett az adatbázisban, de a PDF mentése sikertelen volt!\n"
                                   f"Bizonylatszám: {receipt_number}\n"
                                   f"A szállítólevelet a „Szállítólevél újranyomtatása” gombbal később elkészítheted.")
        else:
            messagebox.showwarning("Figyelem","A tranzakció rögzítve lett az adatbázisban, de a PDF mentése sikertelen volt!")
        self.cart.clear()
        self.load_all_parts()
        self.load_transaction_history()
        return True

    def reprint_receipt(self):
        if not require_active_user(self.main_app):
            return False

        dialog = customtkinter.CTkInputDialog(text="Add meg a bizonylatszámot:", title="Szállítólevél újranyomtatása")
        raw_number = (dialog.get_input() or "").strip()
        if not raw_number:
            return False
        if not (raw_number.isascii() and raw_number.isdigit()):
            messagebox.showerror("Hiba", "A bizonylatszám csak számjegyekből állhat!")
            return False

        with Sessionlocal() as session:
            header = session.query(SellHeader).filter(SellHeader.number == int(raw_number)).first()
            if header is None:
                messagebox.showerror("Hiba", f"Nincs {raw_number} számú bizonylat!")
                return False

            items = []
            for sell_item in header.sell_items:
                items.append({
                    "name": sell_item.part.name,
                    "part_number": sell_item.part.part_number,
                    "quantity": sell_item.amount,
                    "price": sell_item.price,
                    "total": sell_item.amount * sell_item.price,
                })
            buyer_name = header.buyer_name or "-"
            receipt_date = header.date
            receipt_number = header.number
            if not items:
                messagebox.showerror("Hiba", f"A(z) {receipt_number} számú bizonylaton nincs tétel!")
                return False

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Szállítólevél mentése"
        )
        if not filepath:
            return False

        if self.generate_batch_receipt(filepath, buyer_name, "Kiadás", receipt_number=receipt_number,
                                       items=items, receipt_date=receipt_date):
            messagebox.showinfo("Siker", f"A(z) {receipt_number} számú szállítólevél újra elkészült!")
            return True
        messagebox.showerror("Hiba", f"A(z) {receipt_number} számú szállítólevél mentése most sem sikerült!")
        return False

    def generate_batch_receipt(self, filepath, buyer_name, cart_type, receipt_number=None, items=None, receipt_date=None):
        if items is None:
            items = self.cart
        if receipt_date is None:
            receipt_date = datetime.datetime.now()
        try:
            qr_parts = []
            if receipt_number is not None:
                qr_parts.append(f"Bizonylatszam: {receipt_number}")
                qr_parts.append(f"Datum: {receipt_date.strftime('%Y-%m-%d %H:%M')}")
                qr_parts.append(f"Tipus: {cart_type}")
            if cart_type == "Kiadás":
                qr_parts.append(f"Vevo: {buyer_name}")
            qr_data = " | ".join(qr_parts)
            qr_img = qrcode.make(qr_data)
            temp_qr_path = "temp_qr.png"
            qr_img.save(temp_qr_path)
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("Arial", "", str(FONT_DIR / "arial.ttf"))
            pdf.add_font("Arial", "B", str(FONT_DIR / "arialbd.ttf"))
            pdf.add_font("Arial", "I", str(FONT_DIR / "ariali.ttf"))

            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, text="Szállítólevél", new_x="LMARGIN", new_y="NEXT", align="center")
            pdf.image(temp_qr_path, x=160, y=10, w=35)
            pdf.ln(10)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, text=f"Dátum: {receipt_date.strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN",
                     new_y="NEXT", align="center")
            pdf.cell(0, 8, text=f"Tranzakció típusa: {cart_type}", new_x="LMARGIN", new_y="NEXT", align="center")
            if receipt_number is not None:
                pdf.cell(0, 8, text=f"Bizonylatszám: {receipt_number}", new_x="LMARGIN", new_y="NEXT", align="center")
            if cart_type == "Kiadás":
                pdf.cell(0, 8, text=f"Vevő neve: {buyer_name}", new_x="LMARGIN", new_y="NEXT", align="center")
            pdf.ln(10)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(40,10, "Cikkszám", border=1, align="L")
            pdf.cell(50, 10, "Megnevezés", border=1, align="L")
            pdf.cell(30, 10, "Mennyiség", border=1, align="C")
            pdf.cell(35, 10, "Egységár", border=1, align="R")
            pdf.cell(35, 10, "Összesen", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

            pdf.set_font("Arial", "", 12)
            grand_total = 0
            for item in items:
                safe_name = item["name"][:25] if item.get("name") else "-"
                safe_part_number = item["part_number"][:18] if item.get("part_number") else "-"
                pdf.cell(40,10, safe_part_number, border=1, align="L")
                pdf.cell(50, 10, safe_name, border=1, align="L")
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

            if os.path.exists(temp_qr_path):
                os.remove(temp_qr_path)
            return True
        except Exception as e:
            print(f"Hiba a pdf generálásakor: {e}")
            return False

    def valid_quantity(self, raw_quantity):
        if not raw_quantity or not raw_quantity.isascii() or not raw_quantity.isdigit():
            return False
        try:
            return int(raw_quantity) > 0
        except ValueError:
            return False