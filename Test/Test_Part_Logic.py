import unittest
from Controller.PartsController import PartsController
from Model.database import Sessionlocal, Parts

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

class DummyView:
    def __init__(self):
        self.add_button = DummyButton()
        self.delete_button = DummyButton()
        self.edit_button = DummyButton()
        self.tree = DummyTree()

class DummyApp:
    pass

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
        self.manufacturer_cb = DummyVar("Teszt Gyártó")

    def destroy(self):
        pass

class DummyEditView:
    def __init__(self):
        self.part_number = DummyVar("TEST-CREATE-001")
        self.name = DummyVar("Új Fék")
        self.type = DummyVar("Fék")
        self.price = DummyVar(6000)
        self.amount = DummyVar(5)
        self.manufacturer_cb = DummyVar("Teszt Gyártó")

    def destroy(self):
        pass

class TestPartLogic(unittest.TestCase):
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
            controller.manufacturer_map = {"Teszt Gyártó": 1}

            controller.save_edited_part()

            with Sessionlocal() as session:
                updated_part = session.query(Parts).filter(Parts.id == part_id).first()
                self.assertEqual(updated_part.name, "Új Fék", "A név nem frissült az adatbázisban!")
                self.assertEqual(updated_part.price, 6000, "Az ár nem frissült az adatbázisban!")

if __name__ == '__main__':
    unittest.main()