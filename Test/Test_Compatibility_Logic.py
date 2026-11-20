import unittest
from datetime import date
from unittest.mock import patch
from Controller.CompatibilityController import CompatibilityController
from Controller.model_labels import resolve_model_id, build_model_labels
from Model.database import Modell, Parts, Engine, Sessionlocal, VehicleBrand, Compatibility, MotorCompatibility, \
    Manufacturer, VehicleType, Vehicle
from Test.Test_Base import Test_base
from Test.Test_Part_Logic import DummyApp
from View.CompatibilityView import CompatibilityView

class DummyButton:
    def __init__(self):
        self.command = None
    def configure(self, command=None, **kwargs):
        if command:
            self.command = command

class DummyTree:
    def __init__(self):
        self.removed_item = []
        self.inserted_items = []
    def selection(self):
        return ["Test_Part_ID"]

    def item(self, part_id, option):
        return ["TestFek", "TestMotor", "TestLampa"]

    def selection_remove(self, *args):
        self.removed_item.extend(args)

    def get_children(self):
        return []

    def delete(self, item):
        pass

    def insert(self, parent, index, values, iid=None):
        self.inserted_items.append(values)

class DummyVar:
    def __init__(self, value):
        self.value = value
        self.values = []

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def configure(self, values=None, command=None):
        if values is not None:
            self.values = values

class DummyView:
    def __init__(self):
        self.vehiclebrand_dropdown = DummyVar("VehicleBrand")
        self.vehicletype_dropdown = DummyVar("Jármű Típus")
        self.model_dropdown = DummyVar("Model")
        self.engine_dropdown = DummyVar("[4454] Engine | 2000ccm, 150LE")
        self.save_button = DummyButton()
        self.save_button_label = DummyButton()
        self.search_button = DummyButton()
        self.search_button_label = DummyButton()
        self.msgbox_called = False
        self.parts_tree = DummyTree()

    def show_no_part_msgb(self):
        self.msgbox_called = True

    def after(self, ms, func):
        func()
class MockController:
    def __init__(self):
        self.received_engine = None

    def gets_parts_by_engine(self, engine_id):
        self.received_engine = engine_id

def add_vehicle_with_part(brand_id, model_id, engine_id, part_id, engine_code='Engine', with_compat=True):
    with Sessionlocal() as session:
        session.add_all([
            VehicleBrand(id=brand_id, name="Chevy", country="USA"),
            Modell(id=model_id, name='Model', vehicleBrand_id=brand_id, generation=5, date=date(2021, 6, 1)),
            Engine(id=engine_id, engine_code=engine_code, vehicleBrand_id=brand_id, horse_power=150, ccc=2000,fuel_id=1),
            Parts(id=part_id, name='TestFek', manufacturer_id=1, part_number='T-Leg-01', type='Fék', price=210,amount=1, min_amount=1, max_amount=10),
        ])
        if with_compat:
            session.add(Compatibility(part_id=part_id, modell_id=model_id, engine_id=engine_id))
        session.commit()

class Test_Compatibility_Logic(Test_base):
    @patch('Controller.CompatibilityController.messagebox.showwarning')
    @patch('Controller.CompatibilityController.messagebox.showerror')
    def test_save_compatibility(self, mock_error, mock_warning):
        add_vehicle_with_part(brand_id=4451, model_id=4453, engine_id=4454, part_id=4452, with_compat=False)
        view = DummyView()
        view.engine_dropdown.set("[4454] Engine | 2000ccm, 150LE")
        view.parts_tree.selection = lambda: ["4452"]
        CompatibilityController(DummyApp(), view).save_compatibility()

        self.assertIn("4452", view.parts_tree.removed_item, "A kompatibilitás mentése után a kijelölés nem törlődött!")
        with Sessionlocal() as session:
            self.assertIsNotNone(session.query(Compatibility).filter_by(
                part_id=4452, modell_id=4453, engine_id=4454).first(), "A kapcsolat nem mentődött el!")

    @patch('Controller.CompatibilityController.messagebox.showwarning')
    @patch('Controller.CompatibilityController.messagebox.showerror')
    def test_delete_compatibility(self, mock_error, mock_warning):
        add_vehicle_with_part(brand_id=6661, model_id=6663, engine_id=6664, part_id=6662)
        view = DummyView()
        view.engine_dropdown.set("[6664] Engine | 2000ccm, 150LE")
        view.parts_tree.selection = lambda: ["6662"]
        controller = CompatibilityController(DummyApp(), view)
        controller.gets_parts_by_engine("[6664] Engine | 2000ccm, 150LE")
        controller.delete_compatibility()
        with Sessionlocal() as session:
            self.assertIsNone(session.query(Compatibility).filter_by(part_id=6662, modell_id=6663, engine_id=6664).first(),"A kompatibilitás hozzárendelés nem törlődött az adatbázisból!")

    @patch('Controller.CompatibilityController.messagebox.showerror')
    def test_load_all_parts(self, mock_error):
        with Sessionlocal() as session:
            session.add(Parts(id=3332, name='TestFek', manufacturer_id=1, part_number='T-Leg-01', type='Fék',price=210, amount=1, min_amount=1, max_amount=10))
            session.commit()

        view = DummyView()
        CompatibilityController(DummyApp(), view).load_all_parts()

        inserted_names = [item[0] for item in view.parts_tree.inserted_items]
        self.assertIn("TestFek", inserted_names, "Az alkatrész nem töltődött be a táblázatba!")

    def test_load_engines(self):
        with Sessionlocal() as session:
            session.add_all([
                VehicleBrand(id=8881, name="Pontiac", country="USA"),
                Engine(id=8882, engine_code='Engine', vehicleBrand_id=8881, horse_power=150, ccc=2000, fuel_id=1),
                Modell(id=8883, name='FireBird', vehicleBrand_id=8881, generation=5, date=date(2021, 6, 1)),
                MotorCompatibility(modell_id=8883, engine_id=8882),
            ])
            session.commit()

        view = DummyView()
        CompatibilityController(DummyApp(), view).load_engines('FireBird')

        self.assertIn("[8882] Engine | 2000ccm, 150LE", view.engine_dropdown.values,"A motor nem töltődött be a legördülőbe!")

    def test_load_models(self):
        with Sessionlocal() as session:
            session.add_all([
                VehicleType(id=1, name="Személyautó"),
                VehicleBrand(id=5551, name="Chevy", country="USA"),
                Manufacturer(id=9992, name="Bosch"),
                Modell(id=9993, name='Model', vehicleBrand_id=5551, generation=5, date=date(2021, 6, 1)),
                Vehicle(id=1, vehicle_type_id=1, modell_id=9993),
            ])
            session.commit()

        view = DummyView()
        view.vehicletype_dropdown.set("Személyautó")
        CompatibilityController(DummyApp(), view).load_models('Chevy')

        self.assertIn("Model", view.model_dropdown.values, "A modell nem töltődött be a legördülőbe!")

    def test_load_vehiclebrand(self):
        with Sessionlocal() as session:
            session.add_all([
                VehicleType(id=1, name="Személyautó"),
                VehicleBrand(id=5551, name="Chevy", country='USA'),
                Modell(id=9999, name="TesztModell", vehicleBrand_id=5551, generation=1, date=date(2021, 6, 1)),
                Vehicle(id=1, vehicle_type_id=1, modell_id=9999),
            ])
            session.commit()

        view = DummyView()
        CompatibilityController(DummyApp(), view).load_vehiclebrand("Személyautó")

        self.assertIn("Chevy", view.vehiclebrand_dropdown.values, "A márka nem töltődött be a legördülőbe!")

    def test_search_parts_by_engines(self):
        add_vehicle_with_part(brand_id=5556, model_id=5555, engine_id=5552, part_id=5551)

        controller = CompatibilityController(DummyApp(), DummyView())
        found_parts = controller.gets_parts_by_engine("[5552] Engine | 2000ccm, 150LE")

        self.assertIn('TestFek', [part.name for part in found_parts], "A motorhoz rendelt alkatrész nem található!")

    def test_search_update_table(self):
        add_vehicle_with_part(brand_id=5556, model_id=5555, engine_id=5552, part_id=5551, engine_code='coyote v8')

        view = DummyView()
        controller = CompatibilityController(DummyApp(), view)
        view.parts_tree.inserted_items.clear()
        controller.gets_parts_by_engine("[5552] coyote v8 | 2000ccm, 150LE")
        inserted_names = [item[0] for item in view.parts_tree.inserted_items]
        self.assertIn("TestFek", inserted_names, "Az alkatrész nem töltődött be a táblázatba!")

    def test_search_no_found(self):
        view = DummyView()
        CompatibilityController(DummyApp(), view).gets_parts_by_engine("[9999] NEMLETEZOMOTOR | 1000ccm, 100LE")
        self.assertTrue(view.msgbox_called, "Találat nélkül üzenetet kell megjeleníteni!")

    def test_search_action_passes_engine(self):
        controller = MockController()
        real_view = CompatibilityView(master=None)
        real_view.controller = controller

        real_view.engine_dropdown.set(value="[1] coyote v8 | 5000ccm, 500LE")
        real_view.search_action()

        self.assertEqual("[1] coyote v8 | 5000ccm, 500LE", controller.received_engine, "A nézet nem a kiválasztott motort adta át a vezérlőnek!")

    @patch('View.CompatibilityView.messagebox.showwarning')
    def test_search_action_empty(self, mock_showerror):
        controller = MockController()
        real_view = CompatibilityView(master=None)
        real_view.controller = controller

        real_view.engine_dropdown.set(value="")
        real_view.search_action()
        self.assertTrue(mock_showerror.called, "Üres motormező esetén hibaüzenet kell!")
        self.assertIsNone(controller.received_engine, "Üres motormezővel nem indulhat keresés!")

    def test_same_name_engines_are_separate(self):
        with Sessionlocal() as session:
            session.add_all([
                VehicleBrand(id=1, name="VW", country="DE"),
                Modell(id=1, name="Golf", vehicleBrand_id=1, generation=7, date=date(2012, 1, 1)),
                Engine(id=1, engine_code="2.0 TDI", vehicleBrand_id=1, horse_power=150, ccc=1968, fuel_id=1),
                Engine(id=2, engine_code="2.0 TDI", vehicleBrand_id=1, horse_power=190, ccc=1968, fuel_id=1),
                MotorCompatibility(modell_id=1, engine_id=1),
                MotorCompatibility(modell_id=1, engine_id=2),
                Parts(id=1, name="Fékbetét", manufacturer_id=1, part_number="X-1", type="Fék",
                      price=1000, amount=1, min_amount=1, max_amount=2),
                Compatibility(part_id=1, modell_id=1, engine_id=2),
            ])
            session.commit()

        view = DummyView()
        view.model_dropdown.set("Golf")
        controller = CompatibilityController(DummyApp(), view)

        self.assertEqual(1, len(controller.gets_parts_by_engine("[2] 2.0 TDI | 1968ccm, 190LE")))

        view.msgbox_called = False
        controller.gets_parts_by_engine("[1] 2.0 TDI | 1968ccm, 150LE")
        self.assertTrue(view.msgbox_called, "A 150 LE-s motorhoz nem tartozhat alkatrész!")

class TestModelIdentification(Test_base):
    def setUp(self):
        super().setUp()
        with Sessionlocal() as session:
            session.add_all([
                VehicleType(id=1, name="Személyautó"),
                VehicleBrand(id=1, name="Brand A", country="X"),
                VehicleBrand(id=2, name="Brand B", country="Y"),
                Modell(id=1, name="Shared", vehicleBrand_id=1, generation=1, date=date(2020, 1, 1)),
                Modell(id=2, name="Shared", vehicleBrand_id=2, generation=1, date=date(2020, 1, 1)),
                Vehicle(id=1, vehicle_type_id=1, modell_id=1),
                Vehicle(id=2, vehicle_type_id=1, modell_id=2),
                Engine(id=1, engine_code="A-motor", vehicleBrand_id=1, horse_power=100, ccc=1000, fuel_id=1),
                Engine(id=2, engine_code="B-motor", vehicleBrand_id=2, horse_power=200, ccc=2000, fuel_id=1),
                MotorCompatibility(modell_id=1, engine_id=1),
                MotorCompatibility(modell_id=2, engine_id=2),
                Parts(id=1, name="B-alkatrész", manufacturer_id=1, part_number="B-1", type="Fék", price=1000, amount=1, min_amount=1, max_amount=2),
                Compatibility(part_id=1, modell_id=2, engine_id=2),
            ])
            session.commit()

    def test_brand_b_model_shows_brand_b_engine(self):
        view = DummyView()
        view.vehicletype_dropdown.set("Személyautó")
        controller = CompatibilityController(DummyApp(), view)
        controller.load_models("Brand B")
        controller.load_engines(view.model_dropdown.values[0])
        self.assertEqual(["[2] B-motor | 2000ccm, 200LE"], view.engine_dropdown.values, "A Brand B modelljének motorja kell, hogy megjelenjen!")

    def test_parts_filtered_by_model_id(self):
        view = DummyView()
        view.vehicletype_dropdown.set("Személyautó")
        controller = CompatibilityController(DummyApp(), view)
        controller.load_models("Brand A")
        view.model_dropdown.set(view.model_dropdown.values[0])
        result = controller.gets_parts_by_engine("[2] B-motor | 2000ccm, 200LE")

        self.assertTrue(view.msgbox_called, "A Brand A modelljéhez nem tartozhat a Brand B modelljének alkatrésze!")
        self.assertIsNone(result)

    def test_ambiguous_name_is_not_guessed(self):
        with Sessionlocal() as session:
            self.assertIsNone(resolve_model_id(session, "Shared"), "Kétértelmű név esetén nem szabad találomra modellt választani!")

    def test_duplicate_names_get_unique_labels(self):
        with Sessionlocal() as session:
            labels, label_map = build_model_labels(session.query(Modell).all())

        self.assertEqual(2, len(set(labels)), "Azonos nevű modelleknek eltérő feliratot kell kapniuk!")
        self.assertEqual({1, 2}, set(label_map.values()))


if __name__ == '__main__':
    unittest.main()
