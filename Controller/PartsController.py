import math
import os
import shutil
from datetime import date, timedelta
from tkinter import filedialog, messagebox

import customtkinter
from PIL import Image
from sqlalchemy import func

from Model.database import Parts, Sessionlocal, SellItem, SellHeader, Manufacturer
from View.AddPartView import AddPartView
from View.EditPartView import EditPartView


class PartsController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view

        self.view.add_button.configure(command=self.open_add_popup)
        self.view.delete_button.configure(command=self.delete_selected_part)
        self.view.edit_button.configure(command=self.open_edit_popup)

        if hasattr(self.view, "search_entry"):
            self.view.search_entry.bind("<KeyRelease>", self.load_parts)
        if hasattr(self.view, "tree") and hasattr(self.view.tree, "bind"):
            self.view.tree.bind("<<TreeviewSelect>>", self.on_part_select)

        self.view.tree.tag_configure("low_stock",background="red", foreground="white")
        self.view.tree.tag_configure("high_stock", background="green", foreground="white")

        self.selected_edit_id = None
        self.load_parts()

        self.role_permission()

    def role_permission(self):
        current_user = self.main_app.current_user

        if current_user and current_user.role_id == 2:
            for btn in (self.view.add_button, self.view.delete_button, self.view.edit_button):
                if hasattr(btn, "pack_forget"):
                    btn.pack_forget()
                if hasattr(btn, "grid_remove"):
                    btn.grid_remove()

    def get_manufacturer_dict(self):
        with Sessionlocal() as session:
            manufacturers = session.query(Manufacturer).order_by(Manufacturer.name).all()

            result_dict = {}
            for m in manufacturers:
                result_dict[m.name] = m.id
            return result_dict

    def on_part_select(self, event=None):
        if not hasattr(self.view, "preview_image_label"):
            return

        selected = self.view.tree.selection()
        if not selected:
            self.view.preview_image_label.configure(image="", text="Válassz ki egy\nalkatrészt a listából")
            self.view.preview_image_label.image = None
            self.view.preview_name_label.configure(text="")
            self.view.preview_info_label.configure(text="")
            return

        part_id = self.view.tree.item(selected[0])["values"][0]
        with Sessionlocal() as session:
            part = session.query(Parts).filter(Parts.id == part_id).first()
            if not part:
                return

            if part.manufacturer:
                man_name = part.manufacturer.name
            else:
                man_name = "Ismeretlen"
            self.view.preview_name_label.configure(text=part.name)
            self.view.preview_info_label.configure(
                text=f"Cikkszám: {part.part_number}\n"
                     f"Gyártó: {man_name}\n"
                     f"Min. szint: {part.min_amount} db\n"
                     f"Max. szint: {part.max_amount} db"
            )

            if part.image_path and os.path.exists(part.image_path):
                try:
                    pil_img = Image.open(part.image_path)
                    ctk_img = customtkinter.CTkImage(light_image=pil_img, dark_image=pil_img, size=(180, 180))
                    self.view.preview_image_label.configure(image="")
                    self.view.preview_image_label.configure(image=ctk_img, text="")
                    self.view.preview_image_label.image = ctk_img
                except Exception:
                    self.view.preview_image_label.configure(image="", text="Kép nem betölthető")
                    self.view.preview_image_label.image = None
            else:
                self.view.preview_image_label.configure(image="", text="Nincs feltöltött kép")
                self.view.preview_image_label.image = None

    def load_parts(self, *args):
        for parts in self.view.tree.get_children():
            self.view.tree.delete(parts)

        search_term = ""
        if hasattr(self.view, "search_entry"):
            search_term = self.view.search_entry.get().strip()

        with Sessionlocal() as session:
            try:
                query = session.query(Parts)
                if search_term:
                    query = query.filter(
                        (Parts.name.ilike(f"%{search_term}%")) |
                        (Parts.part_number.ilike(f"%{search_term}%"))
                    )
                parts_list = query.order_by(Parts.id).all()
                for part in parts_list:
                    self.part_indicator(part.id)
                    session.refresh(part)
                    if part.amount < part.min_amount:
                        line_tag = ("low_stock",)
                    elif part.amount >= part.max_amount:
                        line_tag = ("high_stock",)
                    else:
                        line_tag = ("normal",)
                    self.view.tree.insert("", "end", values=(part.id, part.part_number, part.name, part.type, part.price, part.amount),tags=line_tag)

            except Exception as e:
                messagebox.showerror("Hiba",f"Hiba történt az adatbázis lekérdezéskor: {e} ")

    def load_low_parts(self):
        with Sessionlocal() as session:
            try:
                return session.query(Parts).filter(Parts.amount < Parts.min_amount).all()
            except Exception as e:
                messagebox.showerror("Hiba",f"Hiba történt az adatbázis lekérdezéskor: {e}")

    def open_add_popup(self):
        if hasattr(self, "add_view") and self.add_view.winfo_exists():
            self.add_view.focus()
            return

        man_dict = self.get_manufacturer_dict()

        self.add_view = AddPartView(self.view, man_dict)
        self.add_view.grab_set()

        self.current_image_path = None
        self.add_view.upload_button.configure(command=self.upload_add_image)
        self.add_view.save_button.configure(command=self.save_part)

    def save_part(self):
        part_num = self.add_view.part_number.get()
        name = self.add_view.name.get()
        part_type = self.add_view.type.get()

        selected_man_name = self.add_view.manufacturer_combobox.get()
        man_id = self.add_view.manufacturer_dict.get(selected_man_name)

        if not man_id:
            messagebox.showerror("Hiba", "Kérlek, válassz egy érvényes gyártót a listából!")
            return

        try:
            price = int(self.add_view.price.get())
            amount = int(self.add_view.amount.get())
            min_amount = int(self.add_view.min_amount.get())
            max_amount = int(self.add_view.max_amount.get())

        except ValueError:
            messagebox.showwarning("Hiba", "Az ár, készlet és gyártó ID mezőkbe csak számot írhatsz!")
            return

        if not part_num or not name or not part_type:
            messagebox.showwarning("Figyelmeztetés","Kérlek tölts ki minden mezőt!")
            return

        new_parts = Parts(
            part_number=part_num,
            name=name,
            type=part_type,
            price=price,
            amount=amount,
            min_amount=min_amount,
            max_amount=max_amount,
            manufacturer_id=man_id,
            image_path= getattr(self, 'current_add_image_path', None)
        )

        with Sessionlocal() as session:
            try:
                session.add(new_parts)
                session.commit()
                messagebox.showinfo("Siker","Sikeresen mentés")
                self.add_view.destroy()
                self.load_parts()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Hiba",f"Hiba történt mentés közben: {e}")

    def upload_image(self):
        filepath = filedialog.askopenfilename(
            title="Válasz egy képet",
            filetypes=[("Képfájlok", "*.png *.jpg *.jpeg")]
        )

        if not filepath:
            return

        os.makedirs("assets/img", exist_ok=True)
        filename = os.path.basename(filepath)
        destination = os.path.join("assets/img", filename)

        shutil.copy(filepath, destination)

        pil_image = Image.open(destination)

        ctk_image = customtkinter.CTkImage(light_image=pil_image,dark_image=pil_image, size=(150,150))

        self.edit_view.image_label.configure(image=ctk_image, text="")
        self.edit_view.image_label.image=ctk_image

        self.current_image_path = destination

    def upload_add_image(self):
        filepath = filedialog.askopenfilename(
            title="Válasz egy képet",
            filetypes=[("Képfájlok", "*.png *.jpg *.jpeg")]
        )

        if not filepath:
            return

        os.makedirs("assets/img", exist_ok=True)
        filename = os.path.basename(filepath)
        destination = os.path.join("assets/img", filename)

        shutil.copy(filepath, destination)

        pil_image = Image.open(destination)

        ctk_image = customtkinter.CTkImage(light_image=pil_image,dark_image=pil_image, size=(150,150))

        self.add_view.image_label.configure(image=ctk_image, text="")
        self.add_view.image_label.image=ctk_image

        self.current_add_image_path = destination

    def open_edit_popup(self):
        if hasattr(self,"edit_view") and self.edit_view.winfo_exists():
            self.edit_view.focus()
            return

        choosed_line = self.view.tree.selection()

        if not choosed_line:
            messagebox.showwarning("Figyelem","Kérlek, válassz ki egy alkatrészt a módosításhoz!")
            return

        if len(choosed_line) > 1:
            messagebox.showerror("Figyelem","Egyszerre csak egy alkatrészt tudsz szerkeszteni!")
            return

        line_datas = self.view.tree.item(choosed_line[0])
        self.selected_edit_id = line_datas['values'][0]

        with Sessionlocal() as session:
            part_to_edit = session.query(Parts).filter(Parts.id == self.selected_edit_id).first()

            if not part_to_edit:
                messagebox.showerror("Hiba","Az alkatrész nem található az adatbázisban!")
                return

            man_dict = self.get_manufacturer_dict()

            self.edit_view = EditPartView(self.view, man_dict)
            self.edit_view.grab_set()
            self.edit_view.part_number.insert(0, part_to_edit.part_number)
            self.edit_view.name.insert(0, part_to_edit.name)
            self.edit_view.type.insert(0, part_to_edit.type)
            self.edit_view.price.insert(0, str(part_to_edit.price))
            self.edit_view.amount.insert(0, str(part_to_edit.amount))
            self.edit_view.min_amount.insert(0, str(part_to_edit.min_amount))
            self.edit_view.max_amount.insert(0,str(part_to_edit.max_amount))
            self.current_image_path = part_to_edit.image_path
            current_man_name = "Válasz egy gyártót..."
            for name, man_id in man_dict.items():
                if man_id == part_to_edit.manufacturer_id:
                    current_man_name = name
                    break
            self.edit_view.manufacturer_combobox.set(current_man_name)
            if self.current_image_path and os.path.exists(self.current_image_path):
                pil_image = Image.open(self.current_image_path)
                ctk_image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(150,150))
                self.edit_view.image_label.configure(image=ctk_image, text="")
                self.edit_view.image_label.image=ctk_image
            else:
                self.edit_view.image_label.configure(text="Nincs kép")

            self.edit_view.upload_button.configure(command=self.upload_image)
            self.edit_view.save_button.configure(command=self.save_edited_part)

    def save_edited_part(self):
        part_num = self.edit_view.part_number.get()
        name = self.edit_view.name.get()
        part_type = self.edit_view.type.get()
        selected_man_name = self.edit_view.manufacturer_combobox.get()
        man_id = self.edit_view.manufacturer_dict.get(selected_man_name)

        if not man_id:
            messagebox.showerror("Hiba", "Kérlek, válassz egy érvényes gyártót a listából!")
            return
        try:
            price = int(self.edit_view.price.get())
            amount = int(self.edit_view.amount.get())
            min_amount = int(self.edit_view.min_amount.get())
            max_amount = int(self.edit_view.max_amount.get())

            if not man_id:
                messagebox.showerror("Hiba","Érvénytelen gyártó!")
                return
        except ValueError:
            messagebox.showwarning("Figyelem","Az ár, készlet és gyártó ID mezőkbe csak számot írhatsz!")
            return

        if not part_num or not name or not part_type:
            messagebox.showwarning("Figyelem","Kérlek tölts ki minden mezőt!")
            return

        new_data = {
            "part_number": part_num,
            "name": name,
            "type": part_type,
            "price": price,
            "amount": amount,
            "min_amount":min_amount,
            "max_amount":max_amount,
            "manufacturer_id": man_id,
            "image_path":  getattr(self, 'current_image_path', None)
        }

        if self.update_part(self.selected_edit_id, new_data):
            messagebox.showinfo("Siker","Sikeresen módosítottad az alkatrészt!")
            self.edit_view.destroy()
            self.load_parts()


    def update_part(self, part_id, new_data):
        with Sessionlocal() as session:
            try:
                part_to_update = session.query(Parts).filter(Parts.id == part_id).first()
                if part_to_update:
                    part_to_update.part_number = new_data['part_number']
                    part_to_update.name = new_data['name']
                    part_to_update.type = new_data['type']
                    part_to_update.price = new_data['price']
                    part_to_update.amount = new_data['amount']
                    part_to_update.min_amount = new_data['min_amount']
                    part_to_update.max_amount = new_data['max_amount']
                    part_to_update.manufacturer_id = new_data['manufacturer_id']
                    part_to_update.image_path = new_data['image_path']
                    session.commit()
                    return True
                else:
                    return False
            except Exception as e:
                session.rollback()
                messagebox.showerror("Hiba",f"Hiba történt a frissítés során: {e}")
                return False

    def delete_selected_part(self):
        choosed_line = self.view.tree.selection()

        if not choosed_line:
            messagebox.showwarning("Figyelem","Kérlek, válassz ki egy alkatrészt a törléshez!")
            return

        successful_delete = False

        for line in choosed_line:
            line_datas = self.view.tree.item(line)
            part_id = line_datas['values'][0]

            if self.delete_part(part_id):
                successful_delete = True
                messagebox.showinfo("Siker",f"Sikeresen törölted a(z) {part_id} azonosítójú alkatrészt!")

        if successful_delete:
            self.load_parts()

    def delete_part(self, part_id):
        with Sessionlocal() as session:
            try:
                part_to_delete = session.query(Parts).filter(Parts.id == part_id).first()
                if part_to_delete:
                    session.delete(part_to_delete)
                    session.commit()
                    return True
                else:
                    return False
            except Exception as e:
                session.rollback()
                messagebox.showerror("Hiba",f"Hiba történt a törlés során: {e}")
                return False

    def part_indicator(self, part_id):
        with Sessionlocal() as session:
            try:
                ninety_days_ago = date.today() - timedelta(days=90)
                total_sold = session.query(func.sum(SellItem.amount)).join(SellHeader).filter(SellHeader.date >= ninety_days_ago,SellItem.part_id == part_id).scalar()
                if total_sold is None:
                    total_sold = 0
                sold_per_day = total_sold / 90.0
                min_sold =math.ceil(sold_per_day * 7)
                max_sold = math.ceil(min_sold*13)
                parts_to_update = session.query(Parts).filter(Parts.id == part_id).first()
                if parts_to_update and total_sold > 0:
                    parts_to_update.min_amount = min_sold
                    parts_to_update.max_amount = max_sold
                    session.commit()
                    return True
                else:
                    return False
            except Exception as e:
                session.rollback()
                messagebox.showerror("Hiba",f"Hiba történt a frissítés során: {e} ")
                return False
