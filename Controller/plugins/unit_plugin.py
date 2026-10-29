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
    plugin_button.grid(row=8, column=0, padx=20, pady=10)

def calculate_mm(inches:float):
    return inches * 25.4

def calculate_liter(gallon:float):
    return gallon * 3.78541

def calculate_bar(psi:float):
    return psi * 0.0689476

def calculate_kw(hp:float):
    return hp * 0.735499

def calculate_nm(lb:float):
    return lb * 1.3558

def open_frame():
    window=customtkinter.CTkToplevel()
    window.title("Mértékegység-váltó")
    window.geometry("400x300")
    window.attributes("-topmost", True)

    title_label = customtkinter.CTkLabel(window, text="Coll (inch) -> Milliméter", font=("Arial", 16, "bold"))
    title_label.pack(pady=15)

    conversion_type = ["Coll -> Miliméter",
                       "Gallon -> Liter",
                       "PSI -> Bar",
                       "Lóerő -> Kilowatt",
                       "Font-láb -> Newtonméter"]


    type_dropdown = customtkinter.CTkOptionMenu(window, values=conversion_type, width=280)
    type_dropdown.pack(pady=10)

    entry = customtkinter.CTkEntry(window, placeholder_text="Átváltandó érték: ", width=280)
    entry.pack(pady=10)

    result_label = customtkinter.CTkLabel(window, text="Eredmény: -mm", font=("Arial", 16, "bold"))
    result_label.pack(pady=10)

    def calculate():
        try:
            value = float(entry.get())
            selected_type = type_dropdown.get()
            if selected_type == "Coll -> Miliméter":
                coll = calculate_mm(value)
                result_label.configure(text=f"Eredmény: {coll:.1f} mm", text_color="white")
            elif selected_type == "Gallon -> Liter":
                gallon = calculate_liter(value)
                result_label.configure(text=f"Eredmény: {gallon:.1f} l", text_color="white")
            elif selected_type == "PSI -> Bar":
                psi = calculate_bar(value)
                result_label.configure(text=f"Eredmény: {psi:.1f} bar", text_color="white")
            elif selected_type == "Lóerő -> Kilowatt":
                hp = calculate_kw(value)
                result_label.configure(text=f"Eredmény: {hp:.1f} bar", text_color="white")
            elif selected_type == "Font-láb -> Newtonméter":
                lb = calculate_nm(value)
                result_label.configure(text=f"Eredmény: {lb:.1f} bar", text_color="white")

        except ValueError:
            result_label.configure(text="Hibás szám!", text_color="red")
    calculate_button = customtkinter.CTkButton(window, text="Átváltás", command=calculate)
    calculate_button.pack(pady=15)