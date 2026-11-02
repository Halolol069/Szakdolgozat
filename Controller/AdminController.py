import datetime
from tkinter import messagebox
import bcrypt
import customtkinter
from sqlalchemy.exc import IntegrityError

from Model.database import (
    Sessionlocal, User, Role, Parts, TransactionLog,
    Manufacturer, VehicleBrand, ROLE_ADMIN, ROLE_WORKER
)


class AdminController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view
        self.view.add_user_btn.configure(command=self.create_user)
        self.view.toggle_status_btn.configure(command=self.toggle_user_status)
        self.view.reset_pw_btn.configure(command=self.reset_user_password)
        self.view.change_role_btn.configure(command=self.toggle_user_role)
        self.view.log_search_entry.bind("<KeyRelease>", self.load_logs)
        self.view.storno_btn.configure(command=self.storno_transaction)
        self.view.add_man_btn.configure(command=self.add_manufacturer)
        self.view.rename_man_btn.configure(command=self.rename_manufacturer)
        self.view.add_brand_btn.configure(command=self.add_brand)
        self.view.update_brand_btn.configure(command=self.update_brand)

        self.load_users()
        self.load_logs()
        self.load_catalog()

    def load_users(self):
        for item in self.view.user_tree.get_children():
            self.view.user_tree.delete(item)

        with Sessionlocal() as session:
            users = session.query(User).order_by(User.id).all()
            for u in users:
                if u.role_id == ROLE_ADMIN:
                    role_name = "Admin"
                else:
                    role_name ="Raktáros"
                is_active = getattr(u, "is_active", True)
                if is_active:
                    status_text = "Aktív"
                else:
                    status_text = "Felfüggesztve"
                self.view.user_tree.insert(
                    "", "end", values=(u.id, u.name, u.email, u.phone, role_name, status_text)
                )

    def create_user(self):

        if not self.main_app.current_user or getattr(self.main_app.current_user, "role_id", None) != ROLE_ADMIN:
            messagebox.showerror("Hiba", "Nincs jogosultságod új felhasználót létrehozni!")
            return

        name = self.view.new_user_name.get().strip()
        email = self.view.new_user_email.get().strip()
        phone = self.view.new_user_phone.get().strip()
        raw_pw = self.view.new_user_pw.get().strip()
        role_str = self.view.new_user_role.get()

        if not all([name, email, phone, raw_pw]):
            messagebox.showerror("Hiba", "Minden mező kitöltése kötelező!")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Hiba", "Az e-mail cím formátuma nem megfelelő (@ és . kötelező)!")
            return

        if len(raw_pw) < 6:
            messagebox.showerror("Hiba", "A jelszó túl rövid, minimum 6 karakter kötelező!")
            return

        if not phone.lstrip("+").isdigit():
            messagebox.showerror("Hiba", "A telefonszám helytelen, csak számokat használj (a + megengedett)!")
            return

        if role_str == "Admin":
            role_id = ROLE_ADMIN
        else:
            role_id = ROLE_WORKER
        hashed_pw = bcrypt.hashpw(raw_pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        with Sessionlocal() as session:
            try:
                new_user = User(
                    name=name, email=email, phone=phone,
                    password=hashed_pw, role_id=role_id, is_active=True
                )
                session.add(new_user)
                session.commit()
                messagebox.showinfo("Siker", f"Felhasználó ({name}) sikeresen létrehozva!")
                self.view.new_user_name.delete(0, "end")
                self.view.new_user_email.delete(0, "end")
                self.view.new_user_phone.delete(0, "end")
                self.view.new_user_pw.delete(0, "end")
                self.load_users()
            except IntegrityError as e:
                session.rollback()
                error = str(e).lower()
                if "users_name_key" in error or "users.name" in error:
                    messagebox.showerror("Hiba", "Ez a felhasználónév már foglalt!")
                elif "users_email_key" in error or "users.email" in error:
                    messagebox.showerror("Hiba", "Ez az e-mail cím már regisztrálva van!")
                elif "users_phone_key" in error or "users.phone" in error:
                    messagebox.showerror("Hiba", "Ez a telefonszám már regisztrálva van!")
                else:
                    messagebox.showerror("Hiba", "A megadott adat már foglalt vagy adatbázis hiba történt!")

    def toggle_user_status(self):
        selected = self.view.user_tree.selection()
        if not selected:
            messagebox.showwarning("Figyelem", "Kérlek válassz ki egy felhasználót a táblázatból!")
            return

        user_id = int(self.view.user_tree.item(selected[0])["values"][0])
        if self.main_app.current_user and self.main_app.current_user.id == user_id:
            messagebox.showerror("Hiba", "Saját magadat nem függesztheted fel!")
            return

        with Sessionlocal() as session:
            user = session.get(User, user_id)
            if user:
                current_status = getattr(user, "is_active", True)
                user.is_active = not current_status
                session.commit()
                if user.is_active:
                    state_str = "aktiválva"
                else:
                    state_str = "felfüggesztve"
                messagebox.showinfo("Siker", f"{user.name} fiókja sikeresen {state_str}!")
                self.load_users()

    def reset_user_password(self):
        selected = self.view.user_tree.selection()
        if not selected:
            messagebox.showwarning("Figyelem", "Kérlek válassz ki egy felhasználót!")
            return

        user_id = int(self.view.user_tree.item(selected[0])["values"][0])
        user_name = self.view.user_tree.item(selected[0])["values"][1]

        dialog = customtkinter.CTkInputDialog(
            text=f"Add meg az új jelszót ({user_name} számára):", title="Jelszó visszaállítása"
        )
        new_pw = dialog.get_input()
        if not new_pw or not new_pw.strip():
            return

        hashed_pw = bcrypt.hashpw(new_pw.strip().encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        with Sessionlocal() as session:
            user = session.get(User, user_id)
            if user:
                user.password = hashed_pw
                session.commit()
                messagebox.showinfo("Siker", f"{user.name} jelszava sikeresen frissítve!")

    def toggle_user_role(self):
        selected = self.view.user_tree.selection()
        if not selected:
            messagebox.showwarning("Figyelem", "Kérlek válassz ki egy felhasználót!")
            return

        user_id = int(self.view.user_tree.item(selected[0])["values"][0])
        if self.main_app.current_user and self.main_app.current_user.id == user_id:
            messagebox.showerror("Hiba", "Saját jogosultságodat nem veheted el!")
            return

        with Sessionlocal() as session:
            user = session.get(User, user_id)
            if user:
                if user.role_id == ROLE_WORKER:
                    user.role_id = ROLE_ADMIN
                else:
                    user.role_id = ROLE_WORKER
                session.commit()
                self.load_users()

    def load_logs(self, event=None):
        for item in self.view.admin_log_tree.get_children():
            self.view.admin_log_tree.delete(item)

        search_term = self.view.log_search_entry.get().strip().lower()

        with Sessionlocal() as session:
            logs = (
                session.query(TransactionLog, Parts.name, User.name)
                .join(Parts, TransactionLog.part_id == Parts.id)
                .join(User, TransactionLog.user_id == User.id)
                .order_by(TransactionLog.date.desc())
                .all()
            )
            for log, part_name, user_name in logs:
                if search_term:
                    haystack = f"{part_name} {user_name} {log.transaction_type}".lower()
                    if search_term not in haystack:
                        continue

                if log.date:
                    date_str = log.date.strftime("%Y-%m-%d %H:%M")
                else:
                    date_str = "-"
                if log.quantity > 0:
                    qty_str = f"+{log.quantity}"
                else:
                    qty_str = str(log.quantity)
                self.view.admin_log_tree.insert(
                    "", "end", values=(log.id, date_str, log.transaction_type, part_name, qty_str, user_name)
                )

    def storno_transaction(self):
        selected = self.view.admin_log_tree.selection()
        if not selected:
            messagebox.showwarning("Figyelem", "Kérlek válassz ki egy tranzakciót a stornózáshoz!")
            return

        log_id = int(self.view.admin_log_tree.item(selected[0])["values"][0])

        with Sessionlocal() as session:
            try:
                log_entry = session.get(TransactionLog, log_id)
                if not log_entry:
                    return

                if "Stornó" in log_entry.transaction_type or "[STORNÓZVA]" in log_entry.transaction_type:
                    messagebox.showerror("Hiba", "Ezt a tételt már korábban stornózták!")
                    return

                part = session.query(Parts).filter(Parts.id == log_entry.part_id).with_for_update().first()
                if not part:
                    messagebox.showerror("Hiba", "A kapcsolódó alkatrész nem található!")
                    return

                reverse_qty = -log_entry.quantity
                if part.amount + reverse_qty < 0:
                    session.rollback()
                    messagebox.showerror(
                        "Hiba",
                        f"A bevételezés nem stornózható, mert negatívba menne a készlet ({part.name}: {part.amount} db)!"
                    )
                    return

                part.amount += reverse_qty
                log_entry.transaction_type = f"{log_entry.transaction_type} [STORNÓZVA]"

                if self.main_app.current_user:
                    admin_id = self.main_app.current_user.id
                else:
                    admin_id = 1
                storno_log = TransactionLog(
                    transaction_type=f"Stornó (#{log_entry.id})",
                    user_id=admin_id,
                    part_id=part.id,
                    quantity=reverse_qty,
                    date=datetime.datetime.now()
                )
                session.add(storno_log)
                session.commit()

                messagebox.showinfo(
                    "Siker",
                    f"A(z) #{log_entry.id} tranzakció stornózva!\n{part.name} új készlete: {part.amount} db."
                )
                self.load_logs()
            except Exception as e:
                session.rollback()
                print("Hiba a stornózás során:", e)
                messagebox.showerror("Hiba", "Váratlan hiba történt a stornózáskor!")

    def load_catalog(self):
        for item in self.view.man_tree.get_children():
            self.view.man_tree.delete(item)
        for item in self.view.brand_tree.get_children():
            self.view.brand_tree.delete(item)

        with Sessionlocal() as session:
            for m in session.query(Manufacturer).order_by(Manufacturer.id).all():
                self.view.man_tree.insert("", "end", values=(m.id, m.name))
            for b in session.query(VehicleBrand).order_by(VehicleBrand.id).all():
                self.view.brand_tree.insert("", "end", values=(b.id, b.name, b.country))

    def add_manufacturer(self):
        name = self.view.man_name_entry.get().strip()
        if not name:
            messagebox.showerror("Hiba", "Add meg a gyártó nevét!")
            return

        with Sessionlocal() as session:
            existing = session.query(Manufacturer).filter(Manufacturer.name.ilike(name)).first()
            if existing:
                messagebox.showerror("Hiba", "Ez a gyártó már szerepel az adatbázisban!")
                return
            session.add(Manufacturer(name=name))
            session.commit()
            self.view.man_name_entry.delete(0, "end")
            self.load_catalog()

    def rename_manufacturer(self):
        selected = self.view.man_tree.selection()
        name = self.view.man_name_entry.get().strip()
        if not selected or not name:
            messagebox.showwarning("Figyelem", "Válassz ki egy gyártót a listából, és írd be az új nevét a mezőbe!")
            return

        man_id = int(self.view.man_tree.item(selected[0])["values"][0])
        with Sessionlocal() as session:
            man = session.get(Manufacturer, man_id)
            if man:
                man.name = name
                session.commit()
                self.view.man_name_entry.delete(0, "end")
                self.load_catalog()

    def add_brand(self):
        name = self.view.brand_name_entry.get().strip()
        country = self.view.brand_country_entry.get().strip()
        if not name or not country:
            messagebox.showerror("Hiba", "Add meg a márka nevét és a származási országot is!")
            return

        with Sessionlocal() as session:
            try:
                session.add(VehicleBrand(name=name, country=country))
                session.commit()
                self.view.brand_name_entry.delete(0, "end")
                self.view.brand_country_entry.delete(0, "end")
                self.load_catalog()
            except IntegrityError:
                session.rollback()
                messagebox.showerror("Hiba", "Ez a járműmárka már létezik!")

    def update_brand(self):
        selected = self.view.brand_tree.selection()
        name = self.view.brand_name_entry.get().strip()
        country = self.view.brand_country_entry.get().strip()
        if not selected or not name or not country:
            messagebox.showwarning("Figyelem", "Válassz ki egy márkát, és töltsd ki az új nevet és országot!")
            return

        brand_id = int(self.view.brand_tree.item(selected[0])["values"][0])
        with Sessionlocal() as session:
            try:
                brand = session.get(VehicleBrand, brand_id)
                if brand:
                    brand.name = name
                    brand.country = country
                    session.commit()
                    self.view.brand_name_entry.delete(0, "end")
                    self.view.brand_country_entry.delete(0, "end")
                    self.load_catalog()
            except IntegrityError:
                session.rollback()
                messagebox.showerror("Hiba", "A megadott márkanév már foglalt!")