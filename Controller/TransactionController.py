from tkinter import messagebox

from Model.database import Sessionlocal, Parts, TransactionLog


class TransactionController:
    def __init__(self, main_app,view):
        self.main_app = main_app
        self.view = view
        self.load_all_parts()
        self.view.save_button.configure(command=self.execute_transaction)
        self.view.search_bar.bind("<KeyRelease>", self.load_all_parts)

    def load_all_parts(self, event=None):
        for item in self.view.transaction_tree.get_children():
            self.view.transaction_tree.delete(item)

        with Sessionlocal() as session:
            try:
                all_parts = session.query(Parts).all()
                search_term = self.view.search_bar.get()
                for part in all_parts:
                    if search_term.lower() in part.name.lower():
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

        if chosed_line:
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

