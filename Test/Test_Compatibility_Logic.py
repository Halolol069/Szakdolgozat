import unittest

from Controller.CompatibilityController import CompatibilityController
from Model.database import Modell, Parts, Engine, Sessionlocal, VehicleBrand, Compatibility, MotorCompatibility, \
    Manufacturer
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
        self.values = []
    def get(self):
        return self.value
    def configure(self, values = None, command = None):
        if values is not None:
            self.values = values

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
            test_vehiclebrand = VehicleBrand(id=4451, name="Lexus", country="USA")
            test_part = Parts(id=4452, name='TestFek', manufacturer_id=1, part_number='T-Leg-01', type='Fék', price=210,
                              amount=1, min_amount=1, max_amount=10)
            test_model = Modell(id=4453, name='Model', vehicleBrand_id=4451, generation=5, date='2021-06-01')
            test_engine = Engine(id=4454, engine_code='Engine', vehicleBrand_id=4451, horse_power=150, ccc=2000,
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
                session.query(Compatibility).filter_by(part_id=4452).delete()
                session.query(Engine).filter_by(id=4454).delete()
                session.query(Modell).filter_by(id=4453).delete()
                session.query(Parts).filter_by(id=4452).delete()
                session.query(VehicleBrand).filter_by(id=4451).delete()
                session.commit()

    def test_load_all_parts(self):
        with Sessionlocal() as session:
            test_part = Parts(id=3332,name='TestFek', manufacturer_id=1, part_number='T-Leg-01', type='Fék', price=210,
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
                    session.query(Parts).filter_by(id=3332).delete()
                    session.commit()

    def test_load_engines(self):
        with Sessionlocal() as session:
            test_vehiclebrand = VehicleBrand(id=8881, name="Pontiac", country="USA")
            test_engine = Engine(id=8882, engine_code='Engine', vehicleBrand_id=8881, horse_power=150, ccc=2000,
                                 fuel_id=1)
            test_model = Modell(id=8883, name='FireBird', vehicleBrand_id=8881, generation=5, date='2021-06-01')
            test_motorCompatibility = MotorCompatibility(modell_id=8883, engine_id=8882)
            session.add_all([test_model,test_engine, test_vehiclebrand, test_motorCompatibility])
            session.commit()

            try:
                mock_app = DummyApp()
                mock_view = DummyView()
                controller = CompatibilityController(mock_app, mock_view)

                controller.load_engines('FireBird')

                self.assertIn("Engine", mock_view.engine_dropdown.values, "A motor nem töltődött be a legördülőbe!")

            finally:
                with Sessionlocal() as session:
                    session.query(MotorCompatibility).filter_by(modell_id=8883, engine_id=8882).delete()
                    session.query(Modell).filter_by(id=8883).delete()
                    session.query(Engine).filter_by(id=8882).delete()
                    session.query(VehicleBrand).filter_by(id=8881).delete()
                    session.commit()

    def test_load_models(self):
        with Sessionlocal() as session:
            test_vehicleBrand = VehicleBrand(id=9991, name="Dodge", country="USA")
            test_manufacturer = Manufacturer(id=9992,name="Bosch")
            test_models = Modell(id=9993, name='Model', vehicleBrand_id=9991, generation=5, date='2021-06-01')
            session.add_all([test_models, test_vehicleBrand, test_manufacturer])
            session.commit()

            try:
                mock_app = DummyApp()
                mock_view = DummyView()
                controller = CompatibilityController(mock_app, mock_view)

                controller.load_models('Dodge')

                self.assertIn("Model", mock_view.model_dropdown.values, "A modell nem töltődött be a legördülőbe!")

            finally:
                with Sessionlocal() as session:
                    session.query(Modell).filter_by(id=9993).delete()
                    session.query(VehicleBrand).filter_by(id=9991).delete()
                    session.query(Manufacturer).filter_by(id=9992).delete()
                    session.commit()

    def test_load_vehiclebrand(self):
        with Sessionlocal() as session:
            test_vehicleBrand = VehicleBrand(id=5551, name="Chevy", country='USA')
            session.add(test_vehicleBrand)
            session.commit()

        try:
            mock_app = DummyApp()
            mock_view = DummyView()
            controller = CompatibilityController(mock_app, mock_view)

            controller.load_vehiclebrand()

            self.assertIn("Chevy", mock_view.vehiclebrand_dropdown.values, "A márka nem töltődött be a legördülőbe!")

        finally:
            with Sessionlocal() as session:
                session.query(VehicleBrand).filter_by(id=5551).delete()
                session.commit()
