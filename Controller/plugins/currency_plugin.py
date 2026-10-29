import customtkinter
def register(app):
    print("Valutaváltó plugin indítása... ")
    try:
        target_frame = app.dashboard.sidebar_frame
    except AttributeError:
        target_frame = app.dashboard

    plugin_button = customtkinter.CTkButton(
        master = target_frame,
        text="Valutaváltó plugin",
        fg_color="green",
        hover_color = "red",
        command=open_currency_window
    )
    plugin_button.grid(row=6, column=0,padx=20, pady=10)

def calculate_huf(euro:float):
    return euro *395

def open_currency_window():
    window = customtkinter.CTkToplevel()
    window.title("Valutaváltó plugin")
    window.geometry("400x300")

    window.attributes("-topmost", True)

    title_label = customtkinter.CTkLabel(window, text="Euró (EUR) -> Forint (HUF)", font=("Arial",16,"bold"))
    title_label.pack(pady=10)

    entry = customtkinter.CTkEntry(window, placeholder_text="Összeg euróban...")
    entry.pack(pady=10)

    result_label = customtkinter.CTkLabel(window, text="Eredmény: -Ft", font=("Arial",14,"bold"))
    result_label.pack(pady=10)

    def calculate():
        try:
            eur = float(entry.get())
            huf = calculate_huf(eur)
            result_label.configure(text=f"Eredmény: {huf:,.0f}Ft")
        except ValueError:
            result_label.configure(text="Kérlek számot adj meg!",text_color="red")

    calc_button = customtkinter.CTkButton(window, text="Számítás", command=calculate)
    calc_button.pack(pady=10)