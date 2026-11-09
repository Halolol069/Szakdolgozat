import unittest
import datetime
from unittest.mock import patch
from Test.Test_Base import Test_base
from Model.database import Sessionlocal, User, Parts, TransactionLog, ROLE_ADMIN
from Controller.AdminController import AdminController

class DummyButton:
    def configure(self, command=None, **kwargs):
        pass

class DummyEntry:
    def bind(self, *args, **kwargs):
        pass
    def get(self):
        return ""

class DummyTree:
    def __init__(self, selected_id):
        self.selected_id = selected_id
    def selection(self):
        return ["item1"]
    def item(self, item_id):
        return {"values": [self.selected_id]}
    def get_children(self):
        return []
    def delete(self, item):
        pass
    def insert(self, *args, **kwargs):
        pass

class DummyAdminView:
    def __init__(self, selected_tree_id=1):
        self.add_user_btn = DummyButton()
        self.toggle_status_btn = DummyButton()
        self.reset_pw_btn = DummyButton()
        self.change_role_btn = DummyButton()
        self.log_search_entry = DummyEntry()
        self.storno_btn = DummyButton()
        self.add_man_btn = DummyButton()
        self.rename_man_btn = DummyButton()
        self.add_brand_btn = DummyButton()
        self.update_brand_btn = DummyButton()
        self.user_tree = DummyTree(selected_tree_id)
        self.admin_log_tree = DummyTree(selected_tree_id)
        self.man_tree = DummyTree(selected_tree_id)
        self.brand_tree = DummyTree(selected_tree_id)

class DummyApp:
    class DummyUser:
        def __init__(self):
            self.id = 99
            self.name = "Fő Admin"
            self.role_id = ROLE_ADMIN
    def __init__(self):
        self.current_user = self.DummyUser()


class Test_Admin_Logic(Test_base):

    @patch('Controller.AdminController.messagebox.showinfo')
    @patch('Controller.AdminController.messagebox.showwarning')
    @patch('Controller.AdminController.messagebox.showerror')
    def test_toggle_user_status(self, mock_error, mock_warning, mock_info):
        with Sessionlocal() as session:
            test_user = User(id=1, name="TesztRaktaros", email="teszt@mail.hu", phone="123", password="hash", role_id=2, is_active=True)
            session.add(test_user)
            session.commit()

        mock_app = DummyApp()
        mock_view = DummyAdminView(selected_tree_id=1)
        controller = AdminController(mock_app, mock_view)

        controller.toggle_user_status()

        with Sessionlocal() as session:
            updated_user = session.get(User, 1)
            self.assertFalse(updated_user.is_active, "A felhasználó státuszának inaktívnak kell lennie!")

    @patch('Controller.AdminController.messagebox.showinfo')
    @patch('Controller.AdminController.messagebox.showwarning')
    @patch('Controller.AdminController.messagebox.showerror')
    def test_storno_transaction(self, mock_error, mock_warning, mock_info):
        with Sessionlocal() as session:
            test_part = Parts(id=1, part_number="ST-01", name="Storno Teszt", type="Teszt", price=1000, amount=7,
                              min_amount=2, max_amount=20, manufacturer_id=1)
            test_log = TransactionLog(id=1, transaction_type="Eladás", user_id=99, part_id=1, quantity=-3,
                                      date=datetime.datetime.now())
            session.add_all([test_part, test_log])
            session.commit()

        mock_app = DummyApp()
        mock_view = DummyAdminView(selected_tree_id=1)
        controller = AdminController(mock_app, mock_view)
        controller.storno_transaction()
        with Sessionlocal() as session:
            updated_part = session.get(Parts, 1)
            self.assertEqual(updated_part.amount, 10, "A stornó után a készletnek vissza kellett állnia 7-ről 10-re!")

            logs = session.query(TransactionLog).filter(TransactionLog.part_id == 1).order_by(TransactionLog.id.desc()).all()
            self.assertEqual(len(logs), 2, "Létre kellett jönnie egy új stornó naplónak!")
            self.assertEqual(logs[0].quantity, 3, "A stornó tranzakció mennyiségének +3-nak kell lennie (az eladás ellentéte)!")
            self.assertIn("Stornó", logs[0].transaction_type, "A tranzakció típusának tartalmaznia kell a Stornó szót!")

if __name__ == '__main__':
    unittest.main()