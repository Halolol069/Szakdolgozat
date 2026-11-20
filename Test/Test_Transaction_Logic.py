import datetime
import unittest
from unittest.mock import patch

from Controller.TransactionController import TransactionController, next_receipt_number
from Model.database import Sessionlocal, Parts, SellHeader, SellItem, TransactionLog, VehicleBrand, Modell, \
    Engine, Compatibility
from Test.Test_Base import Test_base

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


class DummyCombo:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def configure(self, values=None, command=None, **kwargs):
        pass


class DummyTree:
    def __init__(self):
        self.rows = []
    def get_children(self):
        return []

    def delete(self, item):
        pass

    def insert(self, parent, index, values):
        self.rows.append(values)


class DummyView:
    def __init__(self):
        self.to_cart_save_button = DummyButton()
        self.search_bar = DummyEntry()
        self.transaction_tree = DummyTree()
        self.cart_review_button = DummyButton()


class DummyFilterView(DummyView):
    def __init__(self):
        super().__init__()
        self.reset_filter_button = DummyButton()
        self.vehicletype_dropdown = DummyCombo("Jármű típus")
        self.brand_dropdown = DummyCombo("Márka")
        self.model_dropdown = DummyCombo("Modell")
        self.engine_dropdown = DummyCombo("Motor")

class DummyApp:
    def __init__(self):
        self.current_user = self
        self.id = 99

def add_test_part(part_id, name, amount, price=1000):
    with Sessionlocal() as session:
        session.add(Parts(id=part_id, name=name, manufacturer_id=1, part_number=f"T-{part_id}", type="Fék", price=price, amount=amount, min_amount=1, max_amount=20))
        session.commit()


class Test_Transaction_Logic(Test_base):
    def setUp(self):
        super().setUp()
        self.controller = TransactionController(DummyApp(), DummyView())

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
        self.assertFalse(self.controller.valid_quantity("10a"),"A betűket tartalmazó szöveget érvénytelennek kellene tekinteni!")
        self.assertFalse(self.controller.valid_quantity(""), "Az üres mezőt érvénytelennek kellene tekinteni!")

    def test_valid_quantity_superscript(self):
        self.assertFalse(self.controller.valid_quantity("²"), "A felső indexes számjegy nem mennyiség!")
        self.assertFalse(self.controller.valid_quantity("3²"), "A felső indexes számjegy nem mennyiség!")

    @patch('Controller.TransactionController.messagebox.showinfo')
    @patch('Controller.TransactionController.TransactionController.generate_batch_receipt')
    @patch('Controller.TransactionController.filedialog.asksaveasfilename', return_value="teszt.pdf")
    def test_execute_cart_transaction_income(self, *mocks):
        add_test_part(999, "TesztFék", amount=10, price=10000)

        self.controller.cart = [{"part_id": 999, "name": "TesztFék", "type": "Bevételezés", "quantity": 5, "price": 10000, "total": 50000}]
        self.controller.execute_cart_transaction()

        with Sessionlocal() as session:
            self.assertEqual(15, session.get(Parts, 999).amount, "A bevételezés után a mennyiségnek 15-nek kell lennie!")

    @patch('Controller.TransactionController.messagebox.showinfo')
    @patch('Controller.TransactionController.TransactionController.generate_batch_receipt')
    @patch('Controller.TransactionController.filedialog.asksaveasfilename', return_value="teszt.pdf")
    @patch('Controller.TransactionController.customtkinter.CTkInputDialog')
    def test_execute_cart_transaction_expense(self, mock_dialog, *mocks):
        mock_dialog.return_value.get_input.return_value = "Teszt Vevő"
        add_test_part(888, "TesztLámpa", amount=10, price=5000)

        self.controller.cart = [{"part_id": 888, "name": "TesztLámpa", "type": "Kiadás", "quantity": 3, "price": 5000, "total": 15000}]
        self.controller.execute_cart_transaction()

        with Sessionlocal() as session:
            self.assertEqual(7, session.get(Parts, 888).amount)
            self.assertEqual("Teszt Vevő", session.query(SellHeader).first().buyer_name)
            self.assertEqual(1, session.query(SellItem).count())
            self.assertEqual(-3, session.query(TransactionLog).first().quantity)

    @patch('Controller.TransactionController.messagebox.showerror')
    @patch('Controller.TransactionController.filedialog.asksaveasfilename', return_value="teszt.pdf")
    @patch('Controller.TransactionController.customtkinter.CTkInputDialog')
    def test_oversell_rolls_back(self, mock_dialog, mock_save, mock_error):
        mock_dialog.return_value.get_input.return_value = "Vevő"
        add_test_part(777, "Kevés", amount=2)

        self.controller.cart = [{"part_id": 777, "name": "Kevés", "part_number": "T-777", "type": "Kiadás", "quantity": 5, "price": 1000, "total": 5000}]
        result = self.controller.execute_cart_transaction()

        self.assertFalse(result)
        self.assertTrue(mock_error.called)
        with Sessionlocal() as session:
            self.assertEqual(2, session.get(Parts, 777).amount)
            self.assertEqual(0, session.query(SellHeader).count())

    @patch('Controller.TransactionController.messagebox.showinfo')
    @patch('Controller.TransactionController.filedialog.asksaveasfilename', return_value="teszt.pdf")
    @patch('Controller.TransactionController.customtkinter.CTkInputDialog')
    def test_saved_price_equals_pdf_price(self, mock_dialog, *mocks):
        mock_dialog.return_value.get_input.return_value = "Vevő"
        add_test_part(500, "Ártest", amount=10, price=1200)

        self.controller.cart = [{"part_id": 500, "name": "Ártest", "part_number": "T-500", "type": "Kiadás", "quantity": 3, "price": 1000, "total": 3000}]
        pdf_items = []

        def fake_receipt(filepath, buyer_name, cart_type, **kwargs):
            pdf_items.extend(dict(item) for item in self.controller.cart)
            return True

        with patch.object(self.controller, "generate_batch_receipt", side_effect=fake_receipt):
            self.controller.execute_cart_transaction()

        with Sessionlocal() as session:
            item = session.query(SellItem).one()
            self.assertEqual(pdf_items[0]["price"], item.price, "A mentett és a PDF-re kerülő ár eltér!")
            self.assertEqual(pdf_items[0]["total"], item.price * item.amount, "A végösszeg eltér!")

    @patch('Controller.TransactionController.messagebox.showinfo')
    @patch('Controller.TransactionController.filedialog.asksaveasfilename', return_value="teszt.pdf")
    @patch('Controller.TransactionController.customtkinter.CTkInputDialog')
    def test_receipt_number_passed_to_pdf(self, mock_dialog, *mocks):
        mock_dialog.return_value.get_input.return_value = "Vevő"
        add_test_part(600, "Szám", amount=5)

        self.controller.cart = [{"part_id": 600, "name": "Szám", "part_number": "T-600", "type": "Kiadás",
                                 "quantity": 1, "price": 1000, "total": 1000}]
        with patch.object(self.controller, "generate_batch_receipt", return_value=True) as mock_pdf:
            self.controller.execute_cart_transaction()

        with Sessionlocal() as session:
            saved_number = session.query(SellHeader).one().number
        self.assertEqual(saved_number, mock_pdf.call_args.kwargs["receipt_number"],
                         "A PDF-re a mentett bizonylatszámnak kell kerülnie!")

    def test_receipt_number_sqlite_fallback(self):
        with Sessionlocal() as session:
            session.add(SellHeader(id=1, date=datetime.datetime.now(), number=10005))
            session.commit()
            self.assertEqual(10006, next_receipt_number(session))

    @patch('Controller.TransactionController.messagebox.showinfo')
    @patch('Controller.TransactionController.filedialog.asksaveasfilename', return_value="masolat.pdf")
    @patch('Controller.TransactionController.customtkinter.CTkInputDialog')
    def test_reprint_receipt_uses_saved_sale(self, mock_dialog, *mocks):
        mock_dialog.return_value.get_input.return_value = "10001"
        sale_date = datetime.datetime(2026, 11, 1, 10, 30)
        add_test_part(400, "Fékbetét", amount=7, price=1500)
        with Sessionlocal() as session:
            session.add_all([
                SellHeader(id=1, date=sale_date, number=10001, buyer_name="Vevő Kft."),
                SellItem(sell_header_id=1, part_id=400, amount=3, price=1000),
            ])
            session.commit()

        with patch.object(self.controller, "generate_batch_receipt", return_value=True) as mock_pdf:
            self.assertTrue(self.controller.reprint_receipt())

        args, kwargs = mock_pdf.call_args
        self.assertEqual("Vevő Kft.", args[1], "A PDF-re az eredeti vevő neve kell!")
        self.assertEqual(10001, kwargs["receipt_number"])
        self.assertEqual(sale_date, kwargs["receipt_date"], "A PDF-re az eredeti eladás dátuma kell!")
        self.assertEqual(1000, kwargs["items"][0]["price"], "A mentett egységár kell, nem az alkatrész mostani ára!")
        self.assertEqual(3000, kwargs["items"][0]["total"])
        with Sessionlocal() as session:
            self.assertEqual(7, session.get(Parts, 400).amount, "Az újranyomtatás nem módosíthatja a készletet!")
            self.assertEqual(0, session.query(TransactionLog).count(), "Az újranyomtatás nem kerülhet a naplóba!")

    @patch('Controller.TransactionController.messagebox.showerror')
    @patch('Controller.TransactionController.customtkinter.CTkInputDialog')
    def test_reprint_unknown_number_rejected(self, mock_dialog, mock_error):
        mock_dialog.return_value.get_input.return_value = "99999"

        with patch.object(self.controller, "generate_batch_receipt") as mock_pdf:
            self.assertFalse(self.controller.reprint_receipt())

        self.assertTrue(mock_error.called, "Nem létező bizonylatszámnál hibaüzenet kell!")
        self.assertFalse(mock_pdf.called, "Nem létező bizonylatnál nem készülhet PDF!")

    def test_search_stays_within_vehicle_filter(self):
        with Sessionlocal() as session:
            session.add_all([
                VehicleBrand(id=1, name="VW", country="DE"),
                Modell(id=1, name="Golf", vehicleBrand_id=1, generation=7, date=datetime.date(2012, 1, 1)),
                Engine(id=1, engine_code="2.0 TDI", vehicleBrand_id=1, horse_power=150, ccc=1968, fuel_id=1),
                Parts(id=1, part_number="FB-A", name="Fékbetét A", type="Fék", price=1, amount=5, min_amount=1, max_amount=10, manufacturer_id=1),
                Parts(id=2, part_number="FB-B", name="Fékbetét B", type="Fék", price=1, amount=5, min_amount=1, max_amount=10, manufacturer_id=1),
                Compatibility(part_id=1, modell_id=1, engine_id=1),
            ])
            session.commit()

        view = DummyFilterView()
        controller = TransactionController(DummyApp(), view)

        view.model_dropdown.set("Golf")
        view.engine_dropdown.set("[1] 2.0 TDI | 1968ccm, 150LE")
        view.search_bar.value = "Fékbetét"
        view.transaction_tree.rows.clear()
        controller.load_all_parts()
        self.assertEqual([1], [row[0] for row in view.transaction_tree.rows],"Járműszűrés mellett csak a kompatibilis alkatrészek között kell keresni!")

        view.engine_dropdown.set("Motor")
        view.transaction_tree.rows.clear()
        controller.load_all_parts()
        self.assertEqual([1, 2], [row[0] for row in view.transaction_tree.rows],"Szűrés nélkül minden találatnak meg kell jelennie!")


class TestFontPath(unittest.TestCase):
    def test_fonts_found_from_controller_dir(self):
        from Controller.TransactionController import FONT_DIR as transaction_dir
        from Controller.DashboardController import FONT_DIR as dashboard_dir
        for font_dir in (transaction_dir, dashboard_dir):
            for name in ("arial.ttf", "arialbd.ttf", "ariali.ttf"):
                self.assertTrue((font_dir / name).is_file(), f"Hiányzó betűkészlet: {font_dir / name}")


if __name__ == '__main__':
    unittest.main()
