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
    plugin_button.grid(row=7, column=0, padx=20, pady=10)

def open_frame():
    window=customtkinter.CTkToplevel()
    window.title("Mértékegység-váltó")
    window.geometry("400x300")
    window.attributes("-topmost", True)

    title_label = customtkinter.CTkLabel(window, text="Coll (inch) -> Milliméter", font=("Arial", 16, "bold"))
    title_label.pack(pady=15)

    entry = customtkinter.CTkEntry(window, placeholder_text="Méret collban (pl: 17)...")
    entry.pack(pady=10)

    result_label = customtkinter.CTkLabel(window, text="Eredmény: -mm", font=("Arial", 16, "bold"))
    result_label.pack(pady=10)

    def calculate():
        try:
            inches = float(entry.get())
            mm = inches * 25.4
            result_label.configure(text=f"Eredmény: {mm:.1f} mm")
        except ValueError:
            result_label.configure(text="Hibás szám!", text_color="red")
    calculate_button = customtkinter.CTkButton(window, text="Átváltás", command=calculate)
    calculate_button.pack(pady=15)