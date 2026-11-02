import datetime
import unittest
from Controller.PartsController import PartsController
from Model.database import Sessionlocal, Parts, SellHeader, SellItem
from Test.Test_Base import Test_base

class DummyButton:
    def __init__(self):
        self.command = None
    def configure(self, command = None):
        if command:
            self.command = command

class DummyTree:
    def __init__(self):
        self.inserted_rows = []

    def get_children(self):
        return []

    def delete(self,*args, **kwargs):
        pass

    def insert(self,*args, **kwargs):
        if 'values' in kwargs:
            self.inserted_rows.append(kwargs['values'])

    def tag_configure(self, tagname, **kwargs):
        pass

class DummyView:
    def __init__(self):
        self.add_button = DummyButton()
        self.delete_button = DummyButton()
        self.edit_button = DummyButton()
        self.tree = DummyTree()

class DummyApp:
    class DummyUser:
        def __init__(self):
            self.id = 1
            self.name = "Teszt Elek"
            self.role_id = 1

    def __init__(self):
        self.current_user = self.DummyUser()


class DummyVar:
    def __init__(self, value):
        self.value = value
    def get(self):
        return self.value

class DummyAddView:
    def __init__(self):
        self.part_number = DummyVar("TEST-CREATE-001")
        self.name = DummyVar("Teszt új fék")
        self.type = DummyVar("Fék")
        self.price = DummyVar(1000)
        self.amount = DummyVar(5)
        self.min_amount = DummyVar(5)
        self.max_amount = DummyVar(5)
        self.manufacturer_id = DummyVar(1)
        self.manufacturer_combobox = DummyVar("Lemförder")
        self.manufacturer_dict = {"Lemförder": 1}

    def destroy(self):
        pass

class DummyEditView:
    def __init__(self):
        self.part_number = DummyVar("TEST-CREATE-001")
        self.name = DummyVar("Új Fék")
        self.type = DummyVar("Fék")
        self.price = DummyVar(6000)
        self.amount = DummyVar(5)
        self.min_amount = DummyVar(5)
        self.max_amount = DummyVar(5)
        self.manufacturer_id = DummyVar(1)
        self.manufacturer_combobox = DummyVar("Lemförder")
        self.manufacturer_dict = {"Lemförder": 1}

    def destroy(self):
        pass

class TestPartLogic(Test_base):
    def test_read_part(self):
        with Sessionlocal() as session:
            test_part = Parts(
                part_number="TEST-DELETE-001",
                name="Fek",
                type="Fekrendszer",
                price=5000,
                amount=1,
                min_amount=5,
                max_amount=50,
                manufacturer_id=1
            )
            session.add(test_part)
            session.commit()
            part_id = test_part.id
        mock_app = DummyApp()
        mock_view = DummyView()
        controller = PartsController(mock_app, mock_view)

        inserted_rows = mock_view.tree.inserted_rows

        founded = False
        for row in inserted_rows:
            if row[0] == part_id:
                founded = True
                break
        self.assertTrue(founded, "A teszt alkatrész nem töltött be!")

        controller.delete_part(part_id)

    def test_create_part(self):
        mock_app = DummyApp()
        mock_view = DummyView()
        controller = PartsController(mock_app, mock_view)

        controller.add_view = DummyAddView()
        controller.save_part()

        with Sessionlocal() as session:
            created_part = session.query(Parts).filter(Parts.part_number == "TEST-CREATE-001").first()
            self.assertIsNotNone(created_part, "Az új alkatrész nem mentődött el az adatbázisba!")

            if created_part:
                controller.delete_part(created_part.id)

    def test_delete_part(self):
        with Sessionlocal() as session:
            test_part = Parts(
                part_number = "TEST-DELETE-001",
                name= "Fek",
                type = "Fekrendszer",
                price = 5000,
                amount = 1,
                min_amount = 5,
                max_amount = 50,
                manufacturer_id = 1
            )
            session.add(test_part)
            session.commit()
            part_id = test_part.id

        mock_app = DummyApp()
        mock_view = DummyView()

        controller = PartsController(mock_app, mock_view)
        result = controller.delete_part(part_id)

        self.assertTrue(result, "A törlésnek sikeresnek kellett volna lennie!")

        with Sessionlocal() as session:
            deleted_part = session.query(Parts).filter(Parts.id == part_id).first()
            self.assertIsNone(deleted_part, "Még benne van az alkatrész törlés után!")

    def test_update_part(self):
        with Sessionlocal() as session:
            test_part = Parts(
                part_number="TEST-DELETE-001",
                name="Fek",
                type="Fekrendszer",
                price=5000,
                amount=1,
                min_amount=5,
                max_amount=50,
                manufacturer_id=1
            )
            session.add(test_part)
            session.commit()
            part_id = test_part.id

            mock_app = DummyApp()
            mock_view = DummyView()
            controller = PartsController(mock_app, mock_view)

            controller.edit_view = DummyEditView()
            controller.selected_edit_id = part_id

            controller.save_edited_part()

            with Sessionlocal() as session:
                updated_part = session.query(Parts).filter(Parts.id == part_id).first()
                self.assertEqual(updated_part.name, "Új Fék", "A név nem frissült az adatbázisban!")
                self.assertEqual(updated_part.price, 6000, "Az ár nem frissült az adatbázisban!")

    def test_part_indicator(self):
        with Sessionlocal() as session:
            test_part = Parts(
                part_number="TEST-DELETE-001",
                name="Fek",
                type="Fekrendszer",
                price=5000,
                amount=1000,
                min_amount=5,
                max_amount=50,
                manufacturer_id=1
            )

            test_sell_header = SellHeader(
                date=datetime.datetime.now() - datetime.timedelta(days=50),
                number=1
            )
            session.add_all([test_part, test_sell_header])
            session.commit()

            sell_header_id = test_sell_header.id
            part_id = test_part.id
            test_sell_item = SellItem(
                sell_header_id=sell_header_id,
                part_id=part_id,
                amount=100,
                price=5000
            )
            session.add(test_sell_item)
            session.commit()

        mock_app = DummyApp()
        mock_view = DummyView()
        controller = PartsController(mock_app, mock_view)

        controller.part_indicator(part_id)
        with Sessionlocal() as session:
            updated_part = session.query(Parts).filter(Parts.id == part_id).first()
            self.assertEqual(8, updated_part.min_amount, "The min amount is correct")
            self.assertEqual(104, updated_part.max_amount, "The max amount is correct")

if __name__ == '__main__':
    unittest.main()