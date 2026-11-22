import datetime
import unittest
from unittest.mock import patch

from Controller.DashboardController import DashboardController
from Model.database import Sessionlocal, Parts, SellHeader, SellItem
from Test.Test_Base import Test_base

class DummyApp:
    pass

class DummyButton:
    def __init__(self):
        self.command = None

    def configure(self, command=None, **kwargs):
        if command:
            self.command = command

class DummyView:
    def __init__(self):
        self.logout_button = DummyButton()
        self.parts_button = DummyButton()
        self.compatibility_button = DummyButton()
        self.back_button = DummyButton()
        self.transaction_button = DummyButton()
        self.export_pdf_button = DummyButton()
        self.export_csv_button = DummyButton()
        self.admin_button = DummyButton()

class TestDashboardLogic(Test_base):
    def setUp(self):
        super().setUp()
        self.controller = DashboardController(DummyApp(), DummyView())

    def test_low_stock(self):
        with Sessionlocal() as session:
            session.add_all([
                Parts(id=111, part_number="TEST_PART0001", manufacturer_id=1, name="TesztKilincs", type="Váz", price=5000, amount=1, min_amount=2, max_amount=10),
                Parts(id=222, part_number="TEST_PART0002", manufacturer_id=2, name="TesztSzélvédő", type="Váz", price=60000, amount=3, min_amount=2, max_amount=10),
                Parts(id=333, part_number="TEST_PART0003", manufacturer_id=3, name="TesztÉgő", type="Világítás", price=1000, amount=2, min_amount=2, max_amount=10),
            ])
            session.commit()

        result = self.controller.low_stock()

        self.assertEqual(1, len(result), "Pontosan egy alkatrésznek kell a kritikus szint alatt lennie!")
        self.assertEqual(1, result[0][2], "A kritikus alkatrész készlete 1 darab!")

    def test_no_shortage_returns_empty_list(self):
        with Sessionlocal() as session:
            session.add(Parts(id=1, part_number="OK-1", manufacturer_id=1, name="Bőven van", type="Fék", price=1000, amount=50, min_amount=2, max_amount=60))
            session.commit()

        self.assertEqual([], self.controller.low_stock(), "Sikeres vizsgálat hiány nélkül: üres lista!")

    def test_query_error_returns_none(self):
        with patch('Controller.DashboardController.SellItem', new=object()):
            self.assertIsNone(self.controller.low_stock(), "Hiba esetén None-t kell visszaadni, nem üres listát!")

    def test_order_suggestion_from_sales(self):
        now = datetime.datetime.now()
        with Sessionlocal() as session:
            session.add_all([
                Parts(id=1, part_number="FB-1", manufacturer_id=1, name="Fékbetét", type="Fék",
                      price=1000, amount=10, min_amount=5, max_amount=20),
                SellHeader(id=1, date=now - datetime.timedelta(days=10), number=10001),
                SellHeader(id=2, date=now - datetime.timedelta(days=100), number=10002),
                SellItem(sell_header_id=1, part_id=1, amount=180, price=1000),
                SellItem(sell_header_id=2, part_id=1, amount=900, price=1000),
            ])
            session.commit()

        result = self.controller.low_stock()

        self.assertEqual(1, len(result), "A fékbetétnek a dinamikus minimum alatt kell lennie!")
        self.assertEqual(16, result[0][3], "A rendelési javaslatnak 26 - 10 = 16 darabnak kell lennie!")


if __name__ == '__main__':
    unittest.main()
