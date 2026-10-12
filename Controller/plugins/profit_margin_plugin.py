import customtkinter
def register(app):
    print("Árrés kalkulátor betöltése")

    try:
        target_frame = app.dashboard.sidebar_frame
    except AttributeError:
        target_frame = app.dashboard

    plugin_button = customtkinter.CTkButton(
        master=target_frame,
        text="Árrés plugin",
        fg_color="green",
        hover_color="red",
        command=open_margin_window
    )
    plugin_button.grid(row=6, column=0, padx=20, pady=10)

def open_margin_window():
    window = customtkinter.CTkToplevel()
    window.title("Árrés kalkulátor")
    window.geometry("400x300")
    window.attributes("-topmost", True)

    title_label=customtkinter.CTkLabel(window, text="Eladási ár számoló", font=("Arial", 16, "bold"))
    title_label.pack(pady=15)

    net_entry=customtkinter.CTkEntry(window, placeholder_text="Beszerzési ár (%)...")
    net_entry.pack(pady=10)

    margin_entry=customtkinter.CTkEntry(window, placeholder_text="Haszonkulcs (%)...")
    margin_entry.pack(pady=10)

    result_price_label=customtkinter.CTkLabel(window, text="Eladási ár: - Ft",font=("Arial", 16, "bold"))
    result_price_label.pack(pady=10)

    result_profit_label = customtkinter.CTkLabel(window, text="Tiszta haszon: - Ft",font=("Arial", 16, "bold"))
    result_profit_label.pack(pady=5)

    def calculate():
        try:
            net_price = float(net_entry.get())
            margin_percent = float(margin_entry.get())

            profit = net_price * (margin_percent / 100)
            sell_price = net_price + profit

            result_price_label.configure(text=f"Eladási ár: {sell_price:,.0f}Ft")
            result_profit_label.configure(text=f"Tiszta haszon: {profit:,.0f}Ft")

        except ValueError:
            result_price_label.configure(text="Hibás szám!", text_color="red")
            result_profit_label.configure(text="")
    calculate_button = customtkinter.CTkButton(window,text="Kalkuláció", command=calculate)
    calculate_button.pack(pady=15)

