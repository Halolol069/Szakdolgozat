from Model.database import Parts, Sessionlocal
from View.AddPartView import AddPartView


class PartsController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view

        self.view.add_button.configure(command=self.open_add_popup)
        self.view.delete_button.configure(command=self.delete_selected_part)

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
            man_id = int(self.add_view.manufacturer_id.get())
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