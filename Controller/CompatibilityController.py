from tkinter import messagebox

from Model.database import Sessionlocal, VehicleBrand, Modell, Parts, Compatibility, Engine, Vehicle, VehicleType, \
    ROLE_ADMIN


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
                      .filter(VehicleBrand.name == selected_brand,VehicleType.name == selected_type)
                      .all())
            self.model_list = [m.name for m in models]
            self.view.model_dropdown.configure(values=self.model_list, command=self.load_engines)
            self.view.model_dropdown.set("Modell")

    def load_engines(self, selected_model):
        self.view.engine_dropdown.set("Motor")
        with Sessionlocal() as session:
            self.model = session.query(Modell).filter_by(name=selected_model).first()
            if self.model is None:
                messagebox.showwarning("Figyelem", "Előbb válassz ki egy modellt!")
                return

            self.engine_list = []
            for elements in self.model.motor_comps:
                self.engine_list.append(f"[{elements.engine.id}] {elements.engine.engine_code} | {elements.engine.ccc}ccm, {elements.engine.horse_power}LE")
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
                    self.view.parts_tree.insert(parent="",index="end",iid=str(parts.id),values=(parts.name, man_name, parts.type, parts.price))
            except Exception as e:
                messagebox.showerror("Hiba", f"Az alkatrészek betöltése sikertelen: {e}")

    def save_compatibility(self):
        if self.main_app.current_user.role_id != ROLE_ADMIN:
            messagebox.showerror("Hiba", "Nincs jogosultságod kompatibilitást rögzíteni!")
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
            model = session.query(Modell).filter_by(name=model_name).first()
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
        if self.main_app.current_user.role_id != ROLE_ADMIN:
            messagebox.showerror("Hiba", "Nincs jogosultságod kompatibilitást rögzíteni!")
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

        with Sessionlocal() as session:
            try:
                model = session.query(Modell).filter_by(name=model_name).first()
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
                session.commit()
                self.view.save_button_label.configure(text=f"Sikeres törlés ({deleted_count} db)", text_color="green")
                self.view.after(3000, lambda: self.view.save_button_label.configure(text=""))
                self.gets_parts_by_engine(raw_engine)
            except Exception as e:
                session.rollback()
                messagebox.showerror("Hiba", f"Hiba történt a törlés során: {e}")

    def gets_parts_by_engine(self, raw_engine):
        for parts in self.view.parts_tree.get_children():
            self.view.parts_tree.delete(parts)
        if raw_engine == "Motor":
            messagebox.showwarning("Figyelem", "Előbb válassz ki egy motort!")
            return
        engine_id = int(raw_engine.split("]")[0].replace("[", ""))
        selected_model = self.view.model_dropdown.get()

        with Sessionlocal() as session:
            try:
                part_list = (
                    session.query(Parts)
                    .join(Compatibility, Parts.id == Compatibility.part_id)
                    .join(Modell, Compatibility.modell_id == Modell.id)
                    .filter(Compatibility.engine_id == engine_id, Modell.name == selected_model)
                    .all())

                if len(part_list) == 0:
                    return self.view.show_no_part_msgb()
                for parts in part_list:
                    man_name = "None" if parts.manufacturer is None else parts.manufacturer.name
                    self.view.parts_tree.insert(parent="", index="end", iid=str(parts.id),values=(parts.name, man_name, parts.type, parts.price))
                return part_list
            except Exception as e:
                print("Az alkatrészek betöltése sikertelen!", e)