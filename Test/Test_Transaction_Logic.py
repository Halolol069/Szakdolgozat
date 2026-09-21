import unittest
from Controller.TransactionController import TransactionController


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
        self.save_button = DummyButton()
        self.search_bar = DummyEntry()
        self.transaction_tree = DummyTree()


class DummyApp:
    def __init__(self):
        self.current_user = self
        self.id = 1


class Test_Transaction_Logic(unittest.TestCase):
    def setUp(self):
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


if __name__ == '__main__':
    unittest.main()