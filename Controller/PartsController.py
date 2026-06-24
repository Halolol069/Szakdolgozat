from Model.database import Parts, Sessionlocal
from View.AddPartView import AddPartView
from View.EditPartView import EditPartView


class PartsController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view

        self.view.add_button.configure(command=self.open_add_popup)
        self.view.delete_button.configure(command=self.delete_selected_part)
        self.view.edit_button.configure(command=self.open_edit_popup)

        self.selected_edit_id = None
        self.load_parts()

    def load_parts(self):
        for parts in self.view.tree.get_children():
            self.view.tree.delete(parts)

        with Sessionlocal() as session:
            try:
                parts_list = session.query(Parts).all()
                for part in parts_list:
                    self.view.tree.insert("", "end", values=(part.id, part.part_number, part.name, part.type, part.price, part.amount))

            except Exception as e:
                print("Hiba történt az adatbázis lekérdezéskor: ",e)

    def open_add_popup(self):
        self.add_view = AddPartView(self.view)
        self.add_view.save_button.configure(command=self.save_part)

    def save_part(self):
        part_num = self.add_view.part_number.get()
        name = self.add_view.name.get()
        part_type = self.add_view.type.get()

        try:
            price = int(self.add_view.price.get())
            amount = int(self.add_view.amount.get())
            man_id = int(self.add_view.manufacturer_cb.get())
        except ValueError:
            print("Az ár, készlet és gyártó ID mezőkbe csak számot írhatsz!")
            return

        if not part_num or not name or not part_type:
            print("Kérlek tölts ki minden mezőt!")
            return

        new_part = Parts(
            part_number=part_num,
            name=name,
            type=part_type,
            price=price,
            amount=amount,
            min_amount=5,
            max_amount=50,
            manufacturer_id=man_id
        )

        with Sessionlocal() as session:
            try:
                session.add(new_part)
                session.commit()
                print("Sikeresen mentve az adatbázisba!")
                self.add_view.destroy()

                self.load_parts()

            except Exception as e:
                session.rollback()
                print("Hiba történt a mentés során:", e)

    def open_edit_popup(self):
        choosed_line = self.view.tree.selection()

        if not choosed_line:
            print("Kérlek, válassz ki egy alkatrészt a módosításhoz!")
            return

        if len(choosed_line) > 1:
            print("Egyszerre csak egy alkatrészt tudsz szerkeszteni!")
            return

        line_datas = self.view.tree.item(choosed_line[0])
        self.selected_edit_id = line_datas['values'][0]

        with Sessionlocal() as session:
            part_to_edit = session.query(Parts).filter(Parts.id == self.selected_edit_id).first()

            if not part_to_edit:
                print("Az alkatrész nem található az adatbázisban!")
                return

            self.edit_view = EditPartView(self.view)
            self.edit_view.part_number.insert(0, part_to_edit.part_number)
            self.edit_view.name.insert(0, part_to_edit.name)
            self.edit_view.type.insert(0, part_to_edit.type)
            self.edit_view.price.insert(0, str(part_to_edit.price))
            self.edit_view.amount.insert(0, str(part_to_edit.amount))
            self.edit_view.manufacturer_cb.insert(0, str(part_to_edit.manufacturer_id))

            self.edit_view.save_button.configure(command=self.save_edited_part)

    def save_edited_part(self):
        part_num = self.edit_view.part_number.get()
        name = self.edit_view.name.get()
        part_type = self.edit_view.type.get()

        choosed_factory_name = self.edit_view.manufacturer_cb.get()

        try:
            price = int(self.edit_view.price.get())
            amount = int(self.edit_view.amount.get())
            man_id = self.manufacturer_map.get(choosed_factory_name)
            if not man_id:
                print("Érvénytelen gyártó!")
                return
        except ValueError:
            print("Az ár, készlet és gyártó ID mezőkbe csak számot írhatsz!")
            return

        if not part_num or not name or not part_type:
            print("Kérlek tölts ki minden mezőt!")
            return

        new_data = {
            "part_number": part_num,
            "name": name,
            "type": part_type,
            "price": price,
            "amount": amount,
            "manufacturer_id": man_id
        }

        if self.update_part(self.selected_edit_id, new_data):
            print("Sikeresen módosítottad az alkatrészt!")
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
                    part_to_update.manufacturer_id = new_data['manufacturer_id']

                    session.commit()
                    return True
                else:
                    return False
            except Exception as e:
                session.rollback()
                print("Hiba történt a frissítés során: ", e)
                return False

    def delete_selected_part(self):
        choosed_line = self.view.tree.selection()

        if not choosed_line:
            print("Kérlek, válassz ki egy alkatrészt a törléshez!")
            return

        successful_delete = False

        for line in choosed_line:
            line_datas = self.view.tree.item(line)
            part_id = line_datas['values'][0]

            if self.delete_part(part_id):
                successful_delete = True
                print(f"Sikeresen törölted a(z) {part_id} azonosítójú alkatrészt!")

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
                print("Hiba történt a törlés során: ",e)
                return False