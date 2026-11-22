import unittest
from unittest.mock import patch
from Controller.PartsController import PartsController
from Model.database import Sessionlocal, Parts, User, ROLE_ADMIN, ROLE_WORKER
from Test.Test_Base import Test_base, DummyAppWithUser


class DummyButton:
    def __init__(self):
        self.command = None
    def configure(self, command=None):
        if command:
            self.command = command

class DummyEntry:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def bind(self, *args):
        pass

class DummyTree:
    def __init__(self):
        self.inserted_rows = []

    def get_children(self):
        return []

    def delete(self, *args, **kwargs):
        pass

    def insert(self, *args, **kwargs):
        if 'values' in kwargs:
            self.inserted_rows.append(kwargs['values'])

    def tag_configure(self, tagname, **kwargs):
        pass

    def selection(self):
        return ["item1"]

    def item(self, item_id):
        return {"values": [999]}

class DummyView:
    def __init__(self):
        self.add_button = DummyButton()
        self.delete_button = DummyButton()
        self.edit_button = DummyButton()
        self.tree = DummyTree()

class DummyApp:
    class DummyUser:
        def __init__(self):
            self.id = 99
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
        self.location = DummyVar("A-sor, 1.polc")

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
        self.location = DummyVar("B-sor, 2.polc")

    def destroy(self):
        pass


def add_test_part(part_number="TEST-DELETE-001", amount=1, min_amount=5, max_amount=50):
    with Sessionlocal() as session:
        part = Parts(part_number=part_number, name="Fek", type="Fekrendszer", price=5000, amount=amount, min_amount=min_amount, max_amount=max_amount, manufacturer_id=1)
        session.add(part)
        session.commit()
        return part.id

class TestPartLogic(Test_base):
    @patch('Controller.PartsController.messagebox.showinfo')
    @patch('Controller.PartsController.messagebox.showerror')
    def test_read_part(self, mock_error, mock_info):
        part_id = add_test_part()

        view = DummyView()
        PartsController(DummyApp(), view)
        found = any(row[0] == part_id for row in view.tree.inserted_rows)
        self.assertTrue(found, "A teszt alkatrész nem töltött be!")

    @patch('Controller.PartsController.messagebox.showinfo')
    @patch('Controller.PartsController.messagebox.showerror')
    def test_create_part(self, mock_error, mock_info):
        controller = PartsController(DummyApp(), DummyView())
        controller.add_view = DummyAddView()
        controller.save_part()

        with Sessionlocal() as session:
            created_part = session.query(Parts).filter(Parts.part_number == "TEST-CREATE-001").first()
            self.assertIsNotNone(created_part, "Az új alkatrész nem mentődött el az adatbázisba!")
            self.assertEqual("A-sor, 1.polc", created_part.location, "A polchely nem mentődött el helyesen!")

    @patch('Controller.PartsController.messagebox.showinfo')
    @patch('Controller.PartsController.messagebox.showerror')
    def test_delete_part(self, mock_error, mock_info):
        part_id = add_test_part()

        controller = PartsController(DummyApp(), DummyView())
        result = controller.delete_part(part_id)

        self.assertTrue(result, "A törlésnek sikeresnek kellett volna lennie!")
        with Sessionlocal() as session:
            self.assertIsNone(session.get(Parts, part_id), "Még benne van az alkatrész törlés után!")

    @patch('Controller.PartsController.messagebox.showinfo')
    @patch('Controller.PartsController.messagebox.showerror')
    def test_update_part(self, mock_error, mock_info):
        part_id = add_test_part()
        controller = PartsController(DummyApp(), DummyView())
        controller.edit_view = DummyEditView()
        controller.selected_edit_id = part_id
        controller.save_edited_part()
        with Sessionlocal() as session:
            updated_part = session.get(Parts, part_id)
            self.assertEqual("Új Fék", updated_part.name, "A név nem frissült az adatbázisban!")
            self.assertEqual(6000, updated_part.price, "Az ár nem frissült az adatbázisban!")
            self.assertEqual("B-sor, 2.polc", updated_part.location, "A polchely nem frissült az adatbázisban!")

    @patch('Controller.PartsController.messagebox.showinfo')
    @patch('Controller.PartsController.messagebox.showerror')
    def test_edit_does_not_overwrite_stock(self, mock_error, mock_info):
        part_id = add_test_part(amount=10, min_amount=1)
        controller = PartsController(DummyApp(), DummyView())
        controller.edit_view = DummyEditView()
        controller.selected_edit_id = part_id
        with Sessionlocal() as session:
            session.get(Parts, part_id).amount = 7
            session.commit()
        controller.save_edited_part()

        with Sessionlocal() as session:
            updated_part = session.get(Parts, part_id)
            self.assertEqual("Új Fék", updated_part.name, "A névmódosításnak meg kell történnie!")
            self.assertEqual(7, updated_part.amount, "A szerkesztés nem írhatja felül a készletet!")

    @patch('Controller.PartsController.messagebox.showwarning')
    @patch('Controller.PartsController.messagebox.showinfo')
    @patch('Controller.PartsController.messagebox.showerror')
    def test_min_greater_than_max_rejected(self, mock_error, mock_info, mock_warning):
        part_id = add_test_part(amount=3, min_amount=1)
        controller = PartsController(DummyApp(), DummyView())
        controller.edit_view = DummyEditView()
        controller.edit_view.min_amount = DummyVar(20)
        controller.edit_view.max_amount = DummyVar(10)
        controller.selected_edit_id = part_id
        controller.save_edited_part()

        self.assertTrue(mock_warning.called, "Hibás min/max esetén figyelmeztetést kell adni!")
        with Sessionlocal() as session:
            self.assertEqual(1, session.get(Parts, part_id).min_amount, "Hibás min/max nem menthető!")

    def test_search_by_type(self):
        with Sessionlocal() as session:
            session.add_all([
                Parts(id=1, part_number="A-1", name="Betét", type="Fékrendszer", price=1, amount=5, min_amount=1, max_amount=10, manufacturer_id=1),
                Parts(id=2, part_number="B-1", name="Szűrő", type="Szűrő", price=1, amount=5, min_amount=1, max_amount=10, manufacturer_id=1),
            ])
            session.commit()

        view = DummyView()
        view.search_entry = DummyEntry("fékrend")
        PartsController(DummyApp(), view)
        self.assertEqual([1], [row[0] for row in view.tree.inserted_rows], "Típusra is kell tudni keresni!")


class TestPartPermissions(Test_base):
    @patch('Controller.permissions.messagebox.showerror')
    @patch('Controller.PartsController.messagebox.showinfo')
    def test_demoted_admin_cannot_create_part(self, mock_info, mock_perm_error):
        with Sessionlocal() as session:
            session.add(User(id=5, name="volt_admin", password="-", email="v@a.hu", phone="5", role_id=ROLE_WORKER, is_active=True))
            session.commit()

        controller = PartsController(DummyAppWithUser(5, ROLE_ADMIN), DummyView())
        controller.add_view = DummyAddView()
        controller.save_part()

        self.assertTrue(mock_perm_error.called, "Jogosultsághiba üzenetet kell adni!")
        with Sessionlocal() as session:
            self.assertEqual(0, session.query(Parts).count(), "Raktáros nem hozhat létre alkatrészt!")

    @patch('Controller.permissions.messagebox.showerror')
    def test_suspended_admin_cannot_delete_part(self, mock_perm_error):
        with Sessionlocal() as session:
            session.add(User(id=7, name="felfuggesztett", password="-", email="f@a.hu", phone="7", role_id=ROLE_ADMIN, is_active=False))
            session.commit()
        part_id = add_test_part(part_number="DEL-1")
        controller = PartsController(DummyAppWithUser(7, ROLE_ADMIN), DummyView())

        self.assertFalse(controller.delete_part(part_id))
        self.assertTrue(mock_perm_error.called, "Jogosultsághiba üzenetet kell adni!")
        with Sessionlocal() as session:
            self.assertIsNotNone(session.get(Parts, part_id), "Felfüggesztett admin nem törölhet!")


if __name__ == '__main__':
    unittest.main()
