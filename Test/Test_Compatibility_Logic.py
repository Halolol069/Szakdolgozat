import unittest

from Controller.CompatibilityController import CompatibilityController
from Model.database import Modell, Parts, Engine, Sessionlocal, VehicleBrand, Compatibility
from Test.Test_Part_Logic import DummyApp


class DummyDropDown:
    def __init__(self):
        self.command = None
    def configure(self, command = None, **kwargs):
        if command:
            self.command = command

class DummyTree:
    def __init__(self):
        self.removed_item = []
        self.inserted_items = []
    def selection(self):
        return ["Test_Part_ID"]

    def item(self, part_id, option ):
        return ["TestFek", "TestMotor", "TestLampa"]

    def  selection_remove(self,*args):
        for item_id in args:
            self.removed_item.append(item_id)
            pass

    def get_children(self):
        return []

    def delete(self,item):
        pass

    def insert(self, parent, index, values):
        self.inserted_items.append(values)

class DummyVar:
    def __init__(self, value):
        self.value = value
    def get(self):
        return self.value
    def configure(self, values, command):
        return values, command

class DummyView:
    def __init__(self):
        self.vehiclebrand_dropdown = DummyVar("VehicleBrand")
        self.model_dropdown = DummyVar("Model")
        self.engine_dropdown = DummyVar("Engine")
        self.save_button = DummyDropDown()
        self.save_button_label = DummyDropDown()
        self.parts_tree = DummyTree()


class Test_Compatibility_Logic(unittest.TestCase):
    def test_save_compatibility(self):
        with Sessionlocal() as session:
            test_vehiclebrand = VehicleBrand(id=6661, name="LegujabbMarka", country="USA")
            test_part = Parts(id=6662, name='TestFek', manufacturer_id=1, part_number='T-Leg-01', type='Fék', price=210,
                              amount=1, min_amount=1, max_amount=10)
            test_model = Modell(id=6663, name='Model', vehicleBrand_id=6661, generation=5, date='2021-06-01')
            test_engine = Engine(id=6664, engine_code='Engine', vehicleBrand_id=6661, horse_power=150, ccc=2000,
                                 fuel_id=1)
            session.add_all([test_vehiclebrand, test_part, test_model, test_engine])
            session.commit()

        try:
            mock_app = DummyApp()
            mock_view = DummyView()
            controller = CompatibilityController(mock_app, mock_view)

            controller.save_compatibility()

            self.assertIn("Test_Part_ID", mock_view.parts_tree.removed_item,
                          "The selection was not removed from the table after saving the compatibility!")
        finally:
            with Sessionlocal() as session:
                session.query(Compatibility).filter_by(engine_id=6664).delete()
                session.query(Engine).filter_by(id=6664).delete()
                session.query(Modell).filter_by(id=6663).delete()
                session.query(Parts).filter_by(id=6662).delete()
                session.query(VehicleBrand).filter_by(id=6661).delete()
                session.commit()

    def test_load_all_parts(self):
        with Sessionlocal() as session:
            test_part = Parts(id=6662,name='TestFek', manufacturer_id=1, part_number='T-Leg-01', type='Fék', price=210,
                              amount=1, min_amount=1, max_amount=10)
            session.add(test_part)
            session.commit()
            try:
                mock_app = DummyApp()
                mock_view = DummyView()
                controller = CompatibilityController(mock_app, mock_view)

                controller.load_all_parts()

                inserted_names = [item[0] for item in mock_view.parts_tree.inserted_items]
                self.assertIn("TestFek", inserted_names, "Az alkatrész nem töltődött be a táblázatba!")

            finally:
                with Sessionlocal() as session:
                    session.query(Parts).filter_by(id=6662).delete()
                    session.commit()

