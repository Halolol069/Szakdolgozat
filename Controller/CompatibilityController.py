from Model.database import Sessionlocal, VehicleBrand, Modell, Parts, Compatibility, Engine

class CompatibilityController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view
        self.load_vehiclebrand()
        self.load_all_parts()
        self.view.save_button.configure(command=self.save_compatibility)

    def load_vehiclebrand(self):
        with Sessionlocal() as session:
            self.vehiclebrand = session.query(VehicleBrand).all()

            self.vehiclebrand_list = []
            for elements in self.vehiclebrand:
                self.vehiclebrand_list.append(elements.name)
            self.view.vehiclebrand_dropdown.configure(values=self.vehiclebrand_list, command=self.load_models)

    def load_models(self, selected_manufacturer):
        with Sessionlocal() as session:
            self.vehiclebrand = session.query(VehicleBrand).filter_by(name=selected_manufacturer).first()

            self.model_list = []
            for elements in self.vehiclebrand.models:
                self.model_list.append(elements.name)
            self.view.model_dropdown.configure(values=self.model_list, command=self.load_engines)

    def load_engines(self, selected_model):
        with Sessionlocal() as session:
            self.model = session.query(Modell).filter_by(name=selected_model).first()

            self.engine_list = []
            for elements in self.model.motor_comps:
                self.engine_list.append(f"{elements.engine.engine_code},{elements.engine.horse_power}hp, {elements.engine.ccc}ccc")
            self.view.engine_dropdown.configure(values=self.engine_list)

    def load_all_parts(self):
        for parts in self.view.parts_tree.get_children():
            self.view.parts_tree.delete(parts)
        with Sessionlocal() as session:
            try:
                parts_list = session.query(Parts).all()
                for parts in parts_list:
                    if parts.manufacturer is None:
                        man_name = "None"
                    else:
                        man_name = parts.manufacturer.name
                    self.view.parts_tree.insert(parent="",index="end",values=(parts.name, man_name, "", ""))
            except Exception as e:
                print("Failed to load all parts.", e)

    def save_compatibility(self):
        with Sessionlocal() as session:
            self.selected_parts = self.view.parts_tree.selection()
            vehicle_data = {
                "vehiclebrand": self.view.vehiclebrand_dropdown.get(),
                "model": self.view.model_dropdown.get(),
                "engine":self.view.engine_dropdown.get()
            }
            for part_id in self.selected_parts:
                line_data = self.view.parts_tree.item(part_id, "values")
                print(f"{line_data}, {vehicle_data}")
                part = session.query(Parts).filter_by(name=line_data[0]).first()
                model = session.query(Modell).filter_by(name=vehicle_data["model"]).first()
                engine = session.query(Engine).filter_by(engine_code=vehicle_data["engine"]).first()
                new_compatibility = Compatibility(part=part,engine=engine,modell=model)
                session.add(new_compatibility)
                self.view.parts_tree.selection_remove(part_id)
            session.commit()
            if not self.selected_parts:
                self.view.save_button_label.configure(text="Select parts to save failed",text_color="red")
            else:
                self.view.save_button_label.configure(text="Successful save", text_color="green")


