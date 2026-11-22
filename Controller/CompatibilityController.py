from tkinter import messagebox

from Model.database import Sessionlocal, VehicleBrand, Modell, Parts, Compatibility, Vehicle, VehicleType
from Controller.model_labels import build_model_labels, resolve_model_id
from Controller.permissions import require_admin
class CompatibilityController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view
        self.view.controller = self
        self.model_map = {}
        self.listed_vehicle = None
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
        self.view.model_dropdown.configure(values=["Modell"])
        self.view.model_dropdown.set("Modell")
        self.view.engine_dropdown.configure(values=["Motor"])
        self.view.engine_dropdown.set("Motor")
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
        self.view.model_dropdown.set("Modell")
        self.view.engine_dropdown.configure(values=["Motor"])
        self.view.engine_dropdown.set("Motor")
        with Sessionlocal() as session:
            selected_type = self.view.vehicletype_dropdown.get()
            models = (session.query(Modell)
                      .join(VehicleBrand).
                      join(Vehicle).
                      join(VehicleType)
                      .filter(VehicleBrand.name == selected_brand, VehicleType.name == selected_type)
                      .distinct()
                      .all())
            self.model_list, self.model_map = build_model_labels(models)
            self.view.model_dropdown.configure(values=self.model_list, command=self.load_engines)
            self.view.model_dropdown.set("Modell")

    def load_engines(self, selected_model):
        self.view.engine_dropdown.set("Motor")
        with Sessionlocal() as session:
            model_id = resolve_model_id(session, selected_model, self.model_map)
            self.model = session.get(Modell, model_id) if model_id is not None else None
            if self.model is None:
                messagebox.showwarning("Figyelem", "Előbb válassz ki egy modellt!")
                return

            self.engine_list = []
            for elements in self.model.motor_comps:
                self.engine_list.append(f"[{elements.engine.id}] {elements.engine.engine_code} | {elements.engine.ccc}ccm, {elements.engine.horse_power}LE")
            self.view.engine_dropdown.configure(values=self.engine_list)

    def load_all_parts(self):
        self.listed_vehicle = None
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
                    self.view.parts_tree.insert(parent="",index="end",iid=str(parts.id),values=(parts.name, man_name, parts.type, parts.price))
            except Exception as e:
                messagebox.showerror("Hiba", f"Az alkatrészek betöltése sikertelen: {e}")

    def save_compatibility(self):
        if not require_admin(self.main_app):
            return
        with Sessionlocal() as session:
            self.selected_parts = self.view.parts_tree.selection()
            if not self.selected_parts:
                messagebox.showwarning("Figyelem", "Kérlek válassz ki alkatrészeket!")
                return
            raw_engine = self.view.engine_dropdown.get()
            if raw_engine == "Motor":
                messagebox.showwarning("Figyelem", "Előbb válassz ki egy motort!")
                return
            engine_id = int(raw_engine.split("]")[0].replace("[", ""))
            model_name = self.view.model_dropdown.get()
            new_connection = 0
            model_id = resolve_model_id(session, model_name, self.model_map)
            model = session.get(Modell, model_id) if model_id is not None else None
            if model is None:
                messagebox.showwarning("Figyelem", "Előbb válassz ki egy modellt!")
                return
            for part_iid in self.selected_parts:
                part_id = int(part_iid)
                existing = session.query(Compatibility).filter_by(part_id=part_id, engine_id=engine_id,modell_id=model.id).first()
                if not existing:
                    new_compatibility = Compatibility(part_id=part_id, engine_id=engine_id, modell_id=model.id)
                    session.add(new_compatibility)
                    new_connection += 1
                self.view.parts_tree.selection_remove(part_iid)
            session.commit()
            if not self.selected_parts:
                self.view.save_button_label.configure(text="Sikertelen mentés",text_color="red")
            elif new_connection > 0:
                self.view.save_button_label.configure(text="Sikeres mentés", text_color="green")
            else:
                self.view.save_button_label.configure(text="Már létező kapcsolat!", text_color="orange")
            self.view.after(3000, lambda: self.view.save_button_label.configure(text=""))

    def delete_compatibility(self):
        if not require_admin(self.main_app):
            return
        self.selected_parts = self.view.parts_tree.selection()
        if not self.selected_parts:
            messagebox.showwarning("Figyelem", "Kérlek válassz ki alkatrészeket a táblázatból a törléshez!")
            return

        raw_engine = self.view.engine_dropdown.get()
        if raw_engine == "Motor":
            messagebox.showwarning("Figyelem", "Előbb válassz ki egy motort!")
            return
        engine_id = int(raw_engine.split("]")[0].replace("[", ""))
        model_name = self.view.model_dropdown.get()
        if self.listed_vehicle != (model_name, raw_engine):
            messagebox.showwarning("Figyelem", "Előbb a Keresés gombbal listázd ki a járműhöz rendelt alkatrészeket!")
            return
        with Sessionlocal() as session:
            try:
                model_id = resolve_model_id(session, model_name, self.model_map)
                model = session.get(Modell, model_id) if model_id is not None else None
                if not model:
                    messagebox.showerror("Hiba", "Érvénytelen modell!")
                    return

                deleted_count = 0
                for part_iid in self.selected_parts:
                    part_id = int(part_iid)
                    existing = session.query(Compatibility).filter_by(part_id=part_id, engine_id=engine_id,modell_id=model.id).first()
                    if existing:
                        session.delete(existing)
                        deleted_count += 1
                if deleted_count == 0:
                    self.view.save_button_label.configure(text="Nincs törölhető kapcsolat!", text_color="orange")
                    self.view.after(3000, lambda: self.view.save_button_label.configure(text=""))
                    return
                session.commit()
                self.view.save_button_label.configure(text=f"Sikeres törlés ({deleted_count} db)", text_color="green")
                self.view.after(3000, lambda: self.view.save_button_label.configure(text=""))
                self.gets_parts_by_engine(raw_engine)
            except Exception as e:
                session.rollback()
                messagebox.showerror("Hiba", f"Hiba történt a törlés során: {e}")

    def gets_parts_by_engine(self, raw_engine):
        self.listed_vehicle = None
        for parts in self.view.parts_tree.get_children():
            self.view.parts_tree.delete(parts)
        if raw_engine == "Motor":
            messagebox.showwarning("Figyelem", "Előbb válassz ki egy motort!")
            return
        engine_id = int(raw_engine.split("]")[0].replace("[", ""))
        selected_model = self.view.model_dropdown.get()

        with Sessionlocal() as session:
            try:
                model_id = resolve_model_id(session, selected_model, self.model_map)
                if model_id is None:
                    return self.view.show_no_part_msgb()
                part_list = (
                    session.query(Parts)
                    .join(Compatibility, Parts.id == Compatibility.part_id)
                    .filter(Compatibility.engine_id == engine_id, Compatibility.modell_id == model_id)
                    .all())

                if len(part_list) == 0:
                    self.listed_vehicle = None
                    return self.view.show_no_part_msgb()
                self.listed_vehicle = (selected_model, raw_engine)
                for parts in part_list:
                    man_name = "None" if parts.manufacturer is None else parts.manufacturer.name
                    self.view.parts_tree.insert(parent="", index="end", iid=str(parts.id),values=(parts.name, man_name, parts.type, parts.price))
                return part_list
            except Exception as e:
                print("Az alkatrészek betöltése sikertelen!", e)