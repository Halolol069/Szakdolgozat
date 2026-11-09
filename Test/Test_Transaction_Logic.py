import unittest
from Controller.TransactionController import TransactionController
from Model.database import Sessionlocal, Parts, Base, SellHeader, SellItem, TransactionLog
from Test.Test_Base import Test_base
from unittest.mock import patch

class DummyButton:
    def configure(self, command=None, **kwargs):
        pass


class DummyEntry:
    def bind(self, sequence=None, func=None, add=None):
        pass

    def get(self):
        return ""


class DummyTree:
    def get_children(self):
        return []

    def delete(self, item):
        pass

    def insert(self, parent, index, values):
        pass


class DummyView:
    def __init__(self):
        self.to_cart_save_button = DummyButton()
        self.search_bar = DummyEntry()
        self.transaction_tree = DummyTree()
        self.cart_review_button = DummyButton()


class DummyApp:
    def __init__(self):
        self.current_user = self
        self.id = 1


class Test_Transaction_Logic(Test_base):
    def setUp(self):
        super().setUp()
        self.mock_app = DummyApp()
        self.mock_view = DummyView()

        self.controller = TransactionController(self.mock_app, self.mock_view)

    def test_valid_quantity_correct_numbers(self):
        self.assertTrue(self.controller.valid_quantity("10"), "A 10-es számot érvényesnek kellene tekinteni!")
        self.assertTrue(self.controller.valid_quantity("1"), "Az 1-es számot érvényesnek kellene tekinteni!")
        self.assertTrue(self.controller.valid_quantity("999"), "A 999-es számot érvényesnek kellene tekinteni!")

    def test_valid_quantity_zero(self):
        self.assertFalse(self.controller.valid_quantity("0"), "A 0-t érvénytelennek kellene tekinteni!")

    def test_valid_quantity_negative(self):
        self.assertFalse(self.controller.valid_quantity("-5"), "A negatív számokat érvénytelennek kellene tekinteni!")

    def test_valid_quantity_letters_and_empty(self):
        self.assertFalse(self.controller.valid_quantity("öt"), "A betűket érvénytelennek kellene tekinteni!")
        self.assertFalse(self.controller.valid_quantity("10a"),
                         "A betűket tartalmazó szöveget érvénytelennek kellene tekinteni!")
        self.assertFalse(self.controller.valid_quantity(""), "Az üres mezőt érvénytelennek kellene tekinteni!")

    @patch('Controller.TransactionController.messagebox.showinfo')
    @patch('Controller.TransactionController.TransactionController.generate_batch_receipt')
    @patch('Controller.TransactionController.filedialog.asksaveasfilename', return_value="teszt.pdf")
    def test_execute_cart_transaction_income(self,*mock_args):
        with Sessionlocal() as session:
            test_part = Parts(
                id=999, name="TesztFék", manufacturer_id=1, part_number="TF-01",
                type="Fék", price=10000, amount=10, min_amount=2, max_amount=20,
                location="Bevételezés polc"
            )
            session.add(test_part)
            session.commit()

        self.controller.cart = [{
            "part_id": 999, "name": "TesztFék", "type": "Bevételezés",
            "quantity": 5, "price": 10000, "total": 50000
        }]
        self.controller.execute_cart_transaction()

        with Sessionlocal() as session:
            updated_part = session.query(Parts).filter_by(id=999).first()
            self.assertEqual(15, updated_part.amount, "A bevételezés után a mennyiségnek 15-nek kell lennie!")

    @patch('Controller.TransactionController.messagebox.showinfo')
    @patch('Controller.TransactionController.TransactionController.generate_batch_receipt')
    @patch('Controller.TransactionController.filedialog.asksaveasfilename', return_value="teszt.pdf")
    @patch('Controller.TransactionController.customtkinter.CTkInputDialog')
    def test_execute_cart_transaction_expense(self,mock_dialog, *_):
        mock_dialog.return_value.get_input.return_value = "Teszt Vevő"
        with Sessionlocal() as session:
            test_part = Parts(
                id=888, name="TesztLámpa", manufacturer_id=1, part_number="TL-01",
                type="lámpa", price=5000, amount=10, min_amount=2, max_amount=20, location="Kiadás polc"
            )
            session.add(test_part)
            session.commit()

        self.controller.cart = [{
            "part_id": 888, "name": "TesztLámpa", "type": "Kiadás",
            "quantity": 3, "price": 5000, "total": 15000
        }]
        self.controller.execute_cart_transaction()

        with Sessionlocal() as session:
            self.assertEqual(7, session.query(Parts).filter_by(id=888).first().amount)
            self.assertEqual("Teszt Vevő", session.query(SellHeader).first().buyer_name)
            self.assertEqual(1, session.query(SellItem).count())
            self.assertEqual(-3, session.query(TransactionLog).first().quantity)

    @patch('Controller.TransactionController.messagebox.showerror')
    @patch('Controller.TransactionController.filedialog.asksaveasfilename', return_value="teszt.pdf")
    @patch('Controller.TransactionController.customtkinter.CTkInputDialog')
    def test_oversell_rolls_back(self, mock_dialog, mock_save, mock_error):
        mock_dialog.return_value.get_input.return_value = "Vevő"
        with Sessionlocal() as session:
            session.add(Parts(id=777, name="Kevés", manufacturer_id=1, part_number="K-1",
                              type="Fék", price=1000, amount=2, min_amount=1, max_amount=5))
            session.commit()

        self.controller.cart = [{"part_id": 777, "name": "Kevés", "part_number": "K-1",
                                 "type": "Kiadás", "quantity": 5, "price": 1000, "total": 5000}]
        result = self.controller.execute_cart_transaction()

        self.assertFalse(result)
        self.assertTrue(mock_error.called)
        with Sessionlocal() as session:
            self.assertEqual(2, session.query(Parts).filter_by(id=777).first().amount)
            self.assertEqual(0, session.query(SellHeader).count())

    def tearDown(self):
        Base.metadata.drop_all(self.test_engine)
        self.test_engine.dispose()
if __name__ == '__main__':
    unittest.main()