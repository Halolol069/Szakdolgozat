from tkinter import messagebox

from Model.database import Sessionlocal, VehicleBrand, Modell, Parts, Compatibility, Engine, Vehicle, VehicleType

class CompatibilityController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view
        self.view.controller = self
        self.load_vehicletype()
        self.load_all_parts()


    def load_vehicletype(self):
        with Sessionlocal() as session:
            try:
                types = session.query(VehicleType).all()
                self.type_list = [t.name for t in types]
                self.view.vehicletype_dropdown.configure(values=self.type_list, command=self.load_vehiclebrand)
            except Exception as e:
                print("A márka betöltése sikertelen!", e)

    def load_vehiclebrand(self,selected_type):
        self.view.model_dropdown.configure(values=["Model"])
        self.view.engine_dropdown.configure(values=["Motor"])
        with Sessionlocal() as session:
            brands = (session.query(VehicleBrand)
                      .join(Modell).join(Vehicle)
                      .join(VehicleType)
                      .filter(VehicleType.name == selected_type)
                      .distinct()
                      .all())
            self.vehiclebrand_list = [b.name for b in brands]
            self.view.vehiclebrand_dropdown.configure(values=self.vehiclebrand_list, command=self.load_models)
            self.view.vehiclebrand_dropdown.set("Márka")

    def load_models(self, selected_brand):
        self.view.engine_dropdown.configure(values=["Motor"])
        with Sessionlocal() as session:
            selected_type = self.view.vehicletype_dropdown.get()
            models = (session.query(Modell)
                      .join(VehicleBrand).
                      join(Vehicle).
                      join(VehicleType)
                      .filter(VehicleBrand.name == selected_brand,VehicleType.name == selected_type)
                      .all())
            self.model_list = [m.name for m in models]
            self.view.model_dropdown.configure(values=self.model_list, command=self.load_engines)
            self.view.model_dropdown.set("Modell")

    def load_engines(self, selected_model):
        with Sessionlocal() as session:
            self.model = session.query(Modell).filter_by(name=selected_model).first()

            self.engine_list = []
            for elements in self.model.motor_comps:
                self.engine_list.append(f"{elements.engine.engine_code}-{elements.engine.ccc}ccm, {elements.engine.horse_power}LE")
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
                    self.view.parts_tree.insert(parent="",index="end",values=(parts.name, man_name, parts.type, parts.price))
            except Exception as e:
                messagebox.showerror("Az alkatrészek betöltése sikertelen!", e)

    def save_compatibility(self):
        with Sessionlocal() as session:
            self.selected_parts = self.view.parts_tree.selection()
            raw_engine = self.view.engine_dropdown.get()
            engine_code_only = raw_engine.split("-")[0] if "-" in raw_engine else raw_engine
            vehicle_data = {
                "vehiclebrand": self.view.vehiclebrand_dropdown.get(),
                "model": self.view.model_dropdown.get(),
                "engine":engine_code_only
            }
            for part_id in self.selected_parts:
                line_data = self.view.parts_tree.item(part_id, "values")
                print(f"{line_data}, {vehicle_data}")
                part = session.query(Parts).filter_by(name=line_data[0]).first()
                model = session.query(Modell).filter_by(name=vehicle_data["model"]).first()
                engine = session.query(Engine).filter_by(engine_code=vehicle_data["engine"]).first()
                existing = session.query(Compatibility).filter_by(part_id=part.id, engine_id=engine.id, modell_id=model.id).first()
                if not existing:
                    new_compatibility = Compatibility(part=part,engine=engine,modell=model)
                    session.add(new_compatibility)
                self.view.parts_tree.selection_remove(part_id)
            session.commit()
            if not self.selected_parts:
                self.view.save_button_label.configure(text="Sikertelen mentés",text_color="red")
            else:
                self.view.save_button_label.configure(text="Sikeres mentés", text_color="green")
            self.view.after(3000, lambda: self.view.save_button_label.configure(text=""))

    def delete_compatibility(self):
        self.selected_parts = self.view.parts_tree.selection()
        if not self.selected_parts:
            messagebox.showwarning("Figyelem", "Kérlek válassz ki alkatrészeket a táblázatból a törléshez!")
            return

        raw_engine = self.view.engine_dropdown.get()
        engine_code_only = raw_engine.split("-")[0] if "-" in raw_engine else raw_engine

        vehicle_data = {
            "model": self.view.model_dropdown.get(),
            "engine": engine_code_only
        }
        with Sessionlocal() as session:
            try:
                model = session.query(Modell).filter_by(name=vehicle_data["model"]).first()
                engine = session.query(Engine).filter_by(engine_code=vehicle_data["engine"]).first()

                if not model or not engine:
                    messagebox.showerror("Hiba", "Érvénytelen modell vagy motor!")
                    return

                deleted_count = 0
                for part_id in self.selected_parts:
                    line_data = self.view.parts_tree.item(part_id, "values")
                    part = session.query(Parts).filter_by(name=line_data[0]).first()
                    if part:
                        existing = session.query(Compatibility).filter_by(part_id=part.id, engine_id=engine.id, modell_id=model.id).first()
                        if existing:
                            session.delete(existing)
                            deleted_count += 1
                session.commit()
                self.view.save_button_label.configure(text=f"Sikeres törlés ({deleted_count} db)", text_color="green")
                self.view.after(3000, lambda: self.view.save_button_label.configure(text=""))
                self.gets_parts_by_engine(vehicle_data["engine"])

            except Exception as e:
                session.rollback()
                messagebox.showerror("Hiba", f"Hiba történt a törlés során: {e}")

    def gets_parts_by_engine(self,engine_code):
        for parts in self.view.parts_tree.get_children():
                self.view.parts_tree.delete(parts)
        with Sessionlocal() as session:
            try:
                selected_model = self.view.model_dropdown.get()
                part_list = (
                    session.query(Parts)
                    .join(Compatibility, Parts.id == Compatibility.part_id)
                    .join(Engine, Compatibility.engine_id == Engine.id)
                    .join(Modell, Compatibility.modell_id == Modell.id)
                    .filter(Engine.engine_code == engine_code, Modell.name == selected_model)
                    .all())

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
                print("Az alkatrészek betöltése sikertelen!", e)