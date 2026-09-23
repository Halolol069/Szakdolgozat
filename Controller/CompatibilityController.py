from Model.database import Sessionlocal, VehicleBrand, Modell, Parts, Compatibility, Engine, Vehicle, VehicleType


class CompatibilityController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view
        self.view.controller = self
        self.load_vehicletype()
        self.load_all_parts()
        self.view.save_button.configure(command=self.save_compatibility)

    def load_vehicletype(self):
        with Sessionlocal() as session:
            try:
                types = session.query(VehicleType).all()
                self.type_list = [t.name for t in types]
                self.view.vehicletype_dropdown.configure(values=self.type_list, command=self.load_vehiclebrand)
            except Exception as e:
                print("Failed to load vehiclebrand.", e)

    def load_vehiclebrand(self,selected_type):
        self.view.model_dropdown.configure(values=["Model"])
        self.view.engine_dropdown.configure(values=["Motor"])
        with Sessionlocal() as session:
            brands = session.query(VehicleBrand).join(Modell).join(Vehicle).join(VehicleType).filter(VehicleType.name == selected_type).distinct().all()
            self.vehiclebrand_list = [b.name for b in brands]
            self.view.vehiclebrand_dropdown.configure(values=self.vehiclebrand_list, command=self.load_models)
            self.view.vehiclebrand_dropdown.set("Márka")

    def load_models(self, selected_brand):
        self.view.engine_dropdown.configure(values=["Motor"])
        with Sessionlocal() as session:
            selected_type = self.view.vehicletype_dropdown.get()
            models = session.query(Modell).join(VehicleBrand).join(Vehicle).join(VehicleType).filter(VehicleBrand.name == selected_brand,VehicleType.name == selected_type).all()
            self.model_list = [m.name for m in models]
            self.view.model_dropdown.configure(values=self.model_list, command=self.load_engines)
            self.view.model_dropdown.set("Modell")

    def load_engines(self, selected_model):
        with Sessionlocal() as session:
            self.model = session.query(Modell).filter_by(name=selected_model).first()

            self.engine_list = []
            for elements in self.model.motor_comps:
                self.engine_list.append(f"{elements.engine.engine_code}")
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

    def gets_parts_by_engine(self,engine_code):
        for parts in self.view.parts_tree.get_children():
                self.view.parts_tree.delete(parts)
        with Sessionlocal() as session:
            try:
                part_list = session.query(Parts).join(Compatibility).join(Engine).filter(Engine.engine_code == engine_code).all()
                if len(part_list) == 0:
                    return self.view.show_no_part_msgb()
                for parts in part_list:
                    if parts.manufacturer is None:
                        man_name = "None"
                    else:
                        man_name = parts.manufacturer.name
                    self.view.parts_tree.insert(parent="", index="end", values=(parts.name,man_name,parts.type,parts.price))
                return part_list
            except Exception as e:
                print("Failed to load all parts.", e)



