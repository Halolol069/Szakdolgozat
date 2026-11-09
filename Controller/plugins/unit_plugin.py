import customtkinter

def register(app):
    print("Mértékegység-váltó betöltése...")

    try:
        target_frame = app.dashboard.sidebar_frame
    except AttributeError:
        target_frame = app.dashboard

    plugin_button = customtkinter.CTkButton(
        master=target_frame,
        text="Mértékegység plugin",
        fg_color="green",
        hover_color="red",
        command=open_frame
    )
    plugin_button.grid(row=10, column=0, padx=20, pady=10)

def calculate_mm(inches:float):
    return inches * 25.4

def calculate_inch(mm:float):
    return mm / 25.4

def calculate_liter(gallon:float):
    return gallon * 3.78541

def calculate_gallon(liter:float):
    return liter / 3.78541

def calculate_bar(psi:float):
    return psi * 0.0689476

def calculate_psi(bar:float):
    return bar / 0.0689476

def calculate_kw(hp:float):
    return hp * 0.735499

def calculate_hp(kw:float):
    return kw / 0.735499

def calculate_nm(lb:float):
    return lb * 1.3558

def calculate_lbft(nm:float):
    return nm / 1.3558

def open_frame():
    if not hasattr(open_frame, "window") or not open_frame.window.winfo_exists():
        window=customtkinter.CTkToplevel()
        open_frame.window = window
        window.title("Mértékegység-váltó")
        window.geometry("400x300")
        window.attributes("-topmost", True)

        title_label = customtkinter.CTkLabel(window, text="Coll (inch) -> Milliméter", font=("Arial", 16, "bold"))
        title_label.pack(pady=15)

        conversion_type = ["Coll -> Milliméter", "Milliméter -> Coll",
                           "Gallon -> Liter", "Liter -> Gallon",
                           "PSI -> Bar", "Bar -> PSI",
                           "Lóerő -> Kilowatt", "Kilowatt -> Lóerő",
                           "Font-láb -> Newtonméter", "Newtonméter -> Font-láb"]


        type_dropdown = customtkinter.CTkOptionMenu(window, values=conversion_type, width=280)
        type_dropdown.pack(pady=10)
        type_dropdown.set("Coll -> Milliméter")

        entry = customtkinter.CTkEntry(window, placeholder_text="Átváltandó érték: ", width=280)
        entry.pack(pady=10)

        result_label = customtkinter.CTkLabel(window, text="Eredmény: -", font=("Arial", 16, "bold"))
        result_label.pack(pady=10)

        def calculate():
            try:
                value = float(entry.get())
                selected_type = type_dropdown.get()
                if selected_type == "Coll -> Milliméter":
                    coll = calculate_mm(value)
                    result_label.configure(text=f"Eredmény: {coll:.1f} mm", text_color=["black", "white"])
                elif selected_type == "Milliméter -> Coll":
                    inch = calculate_inch(value)
                    result_label.configure(text=f"Eredmény: {inch:.2f} coll", text_color=["black", "white"])

                elif selected_type == "Gallon -> Liter":
                    gallon = calculate_liter(value)
                    result_label.configure(text=f"Eredmény: {gallon:.1f} l", text_color=["black", "white"])
                elif selected_type == "Liter -> Gallon":
                    gal = calculate_gallon(value)
                    result_label.configure(text=f"Eredmény: {gal:.2f} gal", text_color=["black", "white"])

                elif selected_type == "PSI -> Bar":
                    psi = calculate_bar(value)
                    result_label.configure(text=f"Eredmény: {psi:.1f} bar", text_color=["black", "white"])
                elif selected_type == "Bar -> PSI":
                    bar_res = calculate_psi(value)
                    result_label.configure(text=f"Eredmény: {bar_res:.1f} PSI", text_color=["black", "white"])

                elif selected_type == "Lóerő -> Kilowatt":
                    hp = calculate_kw(value)
                    result_label.configure(text=f"Eredmény: {hp:.1f} kW", text_color=["black", "white"])
                elif selected_type == "Kilowatt -> Lóerő":
                    kw = calculate_hp(value)
                    result_label.configure(text=f"Eredmény: {kw:.1f} LE", text_color=["black", "white"])

                elif selected_type == "Font-láb -> Newtonméter":
                    lb = calculate_nm(value)
                    result_label.configure(text=f"Eredmény: {lb:.1f} Nm", text_color=["black", "white"])
                elif selected_type == "Newtonméter -> Font-láb":
                    nm = calculate_lbft(value)
                    result_label.configure(text=f"Eredmény: {nm:.1f} lb-ft", text_color=["black", "white"])

            except ValueError:
                result_label.configure(text="Hibás szám!", text_color="red")
        calculate_button = customtkinter.CTkButton(window, text="Átváltás", command=calculate)
        calculate_button.pack(pady=15)
    else:
        open_frame.window.focus()
        open_frame.window.lift()