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
    plugin_button.grid(row=7, column=0,padx=20, pady=10)

def calculate_huf(euro:float):
    return euro *395

def calculate_dynamic_huf(euro: float, rate: float):
    return euro * rate

def open_currency_window():
    if not hasattr(open_currency_window, "window") or not open_currency_window.window.winfo_exists():
        window = customtkinter.CTkToplevel()
        open_currency_window.window = window
        window.title("Valutaváltó plugin")
        window.geometry("400x300")

        window.attributes("-topmost", True)

        title_label = customtkinter.CTkLabel(window, text="Euró (EUR) -> Forint (HUF)", font=("Arial",16,"bold"))
        title_label.pack(pady=10)

        info_label = customtkinter.CTkLabel(window, text="(Aktuális rögzített árfolyam: 1 EUR = 395 HUF, de átírható!)",font=("Arial", 11, "italic"))
        info_label.pack(pady=(0, 10))

        rate_entry = customtkinter.CTkEntry(window, placeholder_text="Árfolyam (HUF)...")
        rate_entry.insert(0, "395")
        rate_entry.pack(pady=5)

        entry = customtkinter.CTkEntry(window, placeholder_text="Összeg euróban...")
        entry.pack(pady=10)

        result_label = customtkinter.CTkLabel(window, text="Eredmény: -Ft", font=("Arial",14,"bold"))
        result_label.pack(pady=10)

        def calculate():
            try:
                eur = float(entry.get())
                rate = float(rate_entry.get())
                huf = calculate_dynamic_huf(eur, rate)
                result_label.configure(text=f"Eredmény: {huf:,.0f}Ft", text_color=["black", "white"])
            except ValueError:
                result_label.configure(text="Kérlek számot adj meg!",text_color="red")

        calc_button = customtkinter.CTkButton(window, text="Számítás", command=calculate)
        calc_button.pack(pady=10)
    else:
        open_currency_window.window.focus()
        open_currency_window.window.lift()