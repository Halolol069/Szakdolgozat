from Model.database import Parts, Sessionlocal
from View.AddPartView import AddPartView


class PartsController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view

        self.view.add_button.configure(command=self.open_add_popup)

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