from Model.database import Sessionlocal, Parts
from Controller.DashboardController import DashboardController
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

class TestDashboardLogic(Test_base):
    def test_low_stock(self):
        with Sessionlocal() as session:
            part1 = Parts(id=111, part_number="TEST_PART0001", manufacturer_id=1, name="TesztKilincs", type="Váz", price=5000, amount=1, min_amount=2, max_amount=10)
            part2 = Parts(id=222, part_number="TEST_PART0002", manufacturer_id=2, name="TesztSzélvédő", type="Váz", price=60000, amount=3, min_amount=2, max_amount=10)
            part3 = Parts(id=333, part_number="TEST_PART0003", manufacturer_id=3, name="TesztÉgő", type="Világítás", price=1000, amount=2, min_amount=2, max_amount=10)
            session.add_all([part1,part2,part3])
            session.commit()

            mock_app = DummyApp()
            mock_view = DummyView()
            controller = DashboardController(mock_app, mock_view)

            eredmeny = controller.low_stock()

            self.assertEqual(1, len(eredmeny), "The result is correct!")
            self.assertEqual(1, eredmeny[0].amount, "The result is correct!")