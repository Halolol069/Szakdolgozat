from Controller.CompatibilityController import CompatibilityController
from Model.database import Modell, Parts, Engine, Sessionlocal, VehicleBrand, Compatibility, MotorCompatibility, \
    Manufacturer, VehicleType, Vehicle
from Test.Test_Base import Test_base
from Test.Test_Part_Logic import DummyApp
from View.CompatibilityView import CompatibilityView
from unittest.mock import patch
from datetime import date

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

    def set(self,value):
        self.value = value

    def configure(self, values = None, command = None):
        if values is not None:
            self.values = values

class DummyView:
    def __init__(self):
        self.vehiclebrand_dropdown = DummyVar("VehicleBrand")
        self.vehicletype_dropdown = DummyVar("Jármű Típus")
        self.model_dropdown = DummyVar("Model")
        self.engine_dropdown = DummyVar("Engine")
        self.save_button = DummyDropDown()
        self.save_button_label = DummyDropDown()
        self.search_button = DummyDropDown()
        self.search_button_label = DummyDropDown()
        self.msgbox_called = False
        self.parts_tree = DummyTree()

    def show_no_part_msgb(self):
        self.msgbox_called = True

class MockController:
    def __init__(self):
        self.received_engine = None

    def gets_parts_by_engine(self,engine_id):
        self.received_engine = engine_id

class Test_Compatibility_Logic(Test_base):
    def test_save_compatibility(self):
        with Sessionlocal() as session:
            test_type = VehicleType(id=1, name="Személyautó")
            test_vehiclebrand = VehicleBrand(id=4451, name="Lexus", country="USA")
            test_part = Parts(id=4452, name='TestFek', manufacturer_id=1, part_number='T-Leg-01', type='Fék', price=210,
                              amount=1, min_amount=1, max_amount=10)
            test_model = Modell(id=4453, name='Model', vehicleBrand_id=4451, generation=5, date=date(2021,6,1))
            test_engine = Engine(id=4454, engine_code='Engine', vehicleBrand_id=4451, horse_power=150, ccc=2000,
                                 fuel_id=1)
            test_vehicle = Vehicle(id=1, vehicle_type_id=1, modell_id=4453)
            session.add_all([test_type,test_vehiclebrand, test_part, test_model, test_engine,test_vehicle])
            session.commit()

            mock_app = DummyApp()
            mock_view = DummyView()
            controller = CompatibilityController(mock_app, mock_view)

            controller.save_compatibility()

            self.assertIn("Test_Part_ID", mock_view.parts_tree.removed_item, "The selection was not removed from the table after saving the compatibility!")

    def test_load_all_parts(self):
        with Sessionlocal() as session:
            test_part = Parts(id=3332,name='TestFek', manufacturer_id=1, part_number='T-Leg-01', type='Fék', price=210,
                              amount=1, min_amount=1, max_amount=10)
            session.add(test_part)
            session.commit()

            mock_app = DummyApp()
            mock_view = DummyView()
            controller = CompatibilityController(mock_app, mock_view)

            controller.load_all_parts()

            inserted_names = [item[0] for item in mock_view.parts_tree.inserted_items]
            self.assertIn("TestFek", inserted_names, "Az alkatrész nem töltődött be a táblázatba!")

    def test_load_engines(self):
        with Sessionlocal() as session:
            test_vehiclebrand = VehicleBrand(id=8881, name="Pontiac", country="USA")
            test_engine = Engine(id=8882, engine_code='Engine', vehicleBrand_id=8881, horse_power=150, ccc=2000,
                                 fuel_id=1)
            test_model = Modell(id=8883, name='FireBird', vehicleBrand_id=8881, generation=5, date=date(2021,6,1))
            test_motorCompatibility = MotorCompatibility(modell_id=8883, engine_id=8882)
            session.add_all([test_model,test_engine, test_vehiclebrand, test_motorCompatibility])
            session.commit()

            mock_app = DummyApp()
            mock_view = DummyView()
            controller = CompatibilityController(mock_app, mock_view)

            controller.load_engines('FireBird')

            self.assertIn("Engine", mock_view.engine_dropdown.values, "A motor nem töltődött be a legördülőbe!")

    def test_load_models(self):
        with Sessionlocal() as session:
            test_type = VehicleType(id=1, name="Személyautó")
            test_vehicleBrand = VehicleBrand(id=5551, name="Chevy", country="USA")
            test_manufacturer = Manufacturer(id=9992,name="Bosch")
            test_models = Modell(id=9993, name='Model', vehicleBrand_id=5551, generation=5, date=date(2021,6,1))
            test_vehicle = Vehicle(id=1, vehicle_type_id=1, modell_id=9993)
            session.add_all([test_type,test_models, test_vehicleBrand, test_manufacturer,test_vehicle])
            session.commit()

            mock_app = DummyApp()
            mock_view = DummyView()

            mock_view.vehicletype_dropdown.set("Személyautó")

            controller = CompatibilityController(mock_app, mock_view)
            controller.load_models('Chevy')

            self.assertIn("Model", mock_view.model_dropdown.values, "A modell nem töltődött be a legördülőbe!")

    def test_load_vehiclebrand(self):
        with Sessionlocal() as session:
            test_type = VehicleType(id=1, name="Személyautó")
            test_vehicleBrand = VehicleBrand(id=5551, name="Chevy", country='USA')
            test_model = Modell(id=9999, name="TesztModell", vehicleBrand_id=5551, generation=1, date=date(2021, 6, 1))
            test_vehicle = Vehicle(id=1, vehicle_type_id=1, modell_id=9999)
            session.add_all([test_type,test_vehicleBrand,test_model,test_vehicle])
            session.commit()

            mock_app = DummyApp()
            mock_view = DummyView()
            controller = CompatibilityController(mock_app, mock_view)

            controller.load_vehiclebrand("Személyautó")

            self.assertIn("Chevy", mock_view.vehiclebrand_dropdown.values, "A márka nem töltődött be a legördülőbe!")

    def test_search_parts_by_engines(self):
        with Sessionlocal() as session:
            test_parts = Parts(id=5551, name='TestFek', manufacturer_id=1, part_number='T-Leg-01', type='Fék', price=210,
                              amount=1, min_amount=1, max_amount=10)
            test_engines = Engine(id=5552, engine_code='Engine', vehicleBrand_id=5556, horse_power=150, ccc=2000,
                                 fuel_id=1)
            test_modell = Modell (id=5555, name='Model', vehicleBrand_id=5556, generation=5, date=date(2021,6,1))
            test_vehicleBrand = VehicleBrand(id=5556, name='Chevy', country='USA')
            test_compatibility = Compatibility(id=5553, part_id=5551, modell_id = 5555, engine_id = 5552)
            session.add_all([test_parts, test_engines, test_modell, test_vehicleBrand, test_compatibility])
            session.commit()

            mock_app = DummyApp()
            mock_view = DummyView()
            controller = CompatibilityController(mock_app, mock_view)

            search_parts = controller.gets_parts_by_engine("Engine")
            parts_list = [names.name for names in search_parts]
            self.assertIn('TestFek', parts_list, "Parts founded")

    def test_search_actions(self):
        mock_controller = MockController()

        real_view = CompatibilityView(master = None)
        real_view.controller = mock_controller

        real_view.engine_dropdown.set(value="coyote v8")
        real_view.search_action()

        self.assertEqual("coyote v8", mock_controller.received_engine , "The engine code is not same")

    def test_search_update_table(self):
        with Sessionlocal() as session:
            test_parts = Parts(id=5551, name='TestFek', manufacturer_id=1, part_number='T-Leg-01', type='Fék',
                               price=210,
                               amount=1, min_amount=1, max_amount=10)
            test_engines = Engine(id=5552, engine_code='coyote v8', vehicleBrand_id=5556, horse_power=150, ccc=2000,
                                  fuel_id=1)
            test_modell = Modell(id=5555, name='Model', vehicleBrand_id=5556, generation=5, date=date(2021,6,1))
            test_vehicleBrand = VehicleBrand(id=5556, name='Chevy', country='USA')
            test_compatibility = Compatibility(id=5553, part_id=5551, modell_id=5555, engine_id=5552)
            session.add_all([test_parts, test_engines, test_modell, test_vehicleBrand, test_compatibility])
            session.commit()

            mock_app = DummyApp()
            mock_view = DummyView()
            controller = CompatibilityController(mock_app, mock_view)

            mock_view.parts_tree.inserted_items.clear()
            controller.gets_parts_by_engine("coyote v8")
            inserted_names = [item[0] for item in mock_view.parts_tree.inserted_items]
            self.assertIn("TestFek", inserted_names, "Az alkatrész nem töltődött be a táblázatba!")

    def test_search_no_found(self):
        mock_app = DummyApp()
        mock_view = DummyView()
        controller = CompatibilityController(mock_app, mock_view)
        controller.gets_parts_by_engine("EZNEMMOTOR")
        self.assertEqual(True,mock_view.msgbox_called, "The messagebox appeared")

    @patch('View.CompatibilityView.messagebox.showerror')
    def test_search_empty(self,mock_showerror):
        mock_controller = MockController()

        real_view = CompatibilityView(master=None)
        real_view.controller = mock_controller

        real_view.engine_dropdown.set(value="")
        real_view.search_action()
        self.assertTrue(mock_showerror.called, "The messagebox appeared")
        self.assertEqual(None,mock_controller.received_engine, "No parts for the engine" )
