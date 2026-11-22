import datetime
import unittest
from unittest.mock import patch

from Controller.AdminController import AdminController
from Model.database import Sessionlocal, User, Parts, TransactionLog, Manufacturer, ROLE_ADMIN, ROLE_WORKER
from Test.Test_Base import Test_base, DummyAppWithUser

class DummyButton:
    def configure(self, command=None, **kwargs):
        pass

class DummyEntry:
    def __init__(self, value=""):
        self.value = value
    def bind(self, *args, **kwargs):
        pass
    def get(self):
        return self.value

    def delete(self, *args):
        self.value = ""

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


def add_sale(user_id=99):
    with Sessionlocal() as session:
        session.add_all([
            Parts(id=1, part_number="ST-01", name="Storno Teszt", type="Teszt", price=1000, amount=7,
                  min_amount=2, max_amount=20, manufacturer_id=1),
            TransactionLog(id=1, transaction_type="Eladás", user_id=user_id, part_id=1, quantity=-3,
                           date=datetime.datetime.now()),
        ])
        session.commit()


class Test_Admin_Logic(Test_base):
    @patch('Controller.AdminController.messagebox.showinfo')
    @patch('Controller.AdminController.messagebox.showwarning')
    @patch('Controller.AdminController.messagebox.showerror')
    def test_toggle_user_status(self, mock_error, mock_warning, mock_info):
        with Sessionlocal() as session:
            session.add(User(id=1, name="TesztRaktaros", email="teszt@mail.hu", phone="123", password="hash",
                             role_id=ROLE_WORKER, is_active=True))
            session.commit()

        AdminController(DummyApp(), DummyAdminView(selected_tree_id=1)).toggle_user_status()

        with Sessionlocal() as session:
            self.assertFalse(session.get(User, 1).is_active, "A felhasználó státuszának inaktívnak kell lennie!")

    @patch('Controller.AdminController.messagebox.showinfo')
    @patch('Controller.AdminController.messagebox.showwarning')
    @patch('Controller.AdminController.messagebox.showerror')
    def test_storno_transaction(self, mock_error, mock_warning, mock_info):
        add_sale()

        AdminController(DummyApp(), DummyAdminView(selected_tree_id=1)).storno_transaction()

        with Sessionlocal() as session:
            self.assertEqual(10, session.get(Parts, 1).amount,
                             "A stornó után a készletnek vissza kellett állnia 7-ről 10-re!")
            logs = (session.query(TransactionLog).filter(TransactionLog.part_id == 1)
                    .order_by(TransactionLog.id.desc()).all())
            self.assertEqual(2, len(logs), "Létre kellett jönnie egy új stornó naplónak!")
            self.assertEqual(3, logs[0].quantity, "A stornó mennyiségének +3-nak kell lennie (az eladás ellentéte)!")
            self.assertIn("Stornó", logs[0].transaction_type, "A tranzakció típusának tartalmaznia kell a Stornó szót!")

    @patch('Controller.AdminController.messagebox.showinfo')
    @patch('Controller.AdminController.messagebox.showwarning')
    @patch('Controller.AdminController.messagebox.showerror')
    def test_second_storno_rejected(self, mock_error, mock_warning, mock_info):
        add_sale()

        controller = AdminController(DummyApp(), DummyAdminView(selected_tree_id=1))
        controller.storno_transaction()
        controller.storno_transaction()

        with Sessionlocal() as session:
            self.assertEqual(10, session.get(Parts, 1).amount, "A készlet csak egyszer állhat vissza!")
            self.assertEqual(1, session.query(TransactionLog).filter(
                TransactionLog.transaction_type == "Stornó (#1)").count(), "Csak egy stornó naplósor lehet!")
        self.assertTrue(mock_error.called, "A második sztornónál hibaüzenetet kell adni!")

    @patch('Controller.AdminController.messagebox.showinfo')
    @patch('Controller.AdminController.messagebox.showwarning')
    @patch('Controller.AdminController.messagebox.showerror')
    def test_rename_manufacturer_to_existing_name_rejected(self, mock_error, mock_warning, mock_info):
        view = DummyAdminView(selected_tree_id=2)
        view.man_name_entry = DummyEntry("bosch")
        AdminController(DummyApp(), view).rename_manufacturer()

        self.assertTrue(mock_error.called, "Foglalt névre átnevezéskor hibaüzenet kell!")
        with Sessionlocal() as session:
            self.assertEqual("Valeo", session.get(Manufacturer, 2).name, "A gyártó neve nem változhat meg!")


class TestAdminPermissions(Test_base):
    @patch('Controller.permissions.messagebox.showerror')
    def test_worker_cannot_storno(self, mock_perm_error):
        with Sessionlocal() as session:
            session.add(User(id=8, name="raktaros8", password="-", email="r@a.hu", phone="8", role_id=ROLE_WORKER, is_active=True))
            session.commit()
        add_sale(user_id=8)

        AdminController(DummyAppWithUser(8, ROLE_WORKER), DummyAdminView(selected_tree_id=1)).storno_transaction()

        self.assertTrue(mock_perm_error.called, "Jogosultsághiba üzenetet kell adni!")
        with Sessionlocal() as session:
            self.assertEqual(7, session.get(Parts, 1).amount, "Raktáros nem sztornózhat!")


if __name__ == '__main__':
    unittest.main()