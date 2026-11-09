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
    plugin_button.grid(row=9, column=0, padx=20, pady=10)

def calculate_margin(net_price: float, margin_percent: float):
    profit = net_price * (margin_percent / 100)
    sell_price = net_price + profit
    return sell_price, profit


def calculate_reverse_margin(net_price: float, sell_price: float):
    profit = sell_price - net_price
    margin_percent = (profit / net_price) * 100 if net_price > 0 else 0
    return margin_percent, profit


def open_margin_window():
    if not hasattr(open_margin_window, "window") or not open_margin_window.window.winfo_exists():
        window = customtkinter.CTkToplevel()
        open_margin_window.window = window
        window.title("Árrés kalkulátor")
        window.geometry("450x420")
        window.attributes("-topmost", True)

        tabview = customtkinter.CTkTabview(window, width=400, height=350)
        tabview.pack(padx=20, pady=10)
        tabview.add("Eladási ár számítás")
        tabview.add("Alkudozás (Visszaszámolás)")

        net_entry1 = customtkinter.CTkEntry(tabview.tab("Eladási ár számítás"),placeholder_text="Beszerzési ár (Ft)...", width=200)
        net_entry1.pack(pady=10)

        margin_entry1 = customtkinter.CTkEntry(tabview.tab("Eladási ár számítás"),placeholder_text="Haszonkulcs (%)...", width=200)
        margin_entry1.pack(pady=10)

        res_price1 = customtkinter.CTkLabel(tabview.tab("Eladási ár számítás"), text="Eladási ár: - Ft",font=("Arial", 16, "bold"))
        res_price1.pack(pady=5)

        res_prof1 = customtkinter.CTkLabel(tabview.tab("Eladási ár számítás"), text="Tiszta haszon: - Ft",font=("Arial", 14))
        res_prof1.pack(pady=5)

        def calc1():
            try:
                net = float(net_entry1.get())
                marg = float(margin_entry1.get())
                sell_price, profit = calculate_margin(net, marg)
                res_price1.configure(text=f"Eladási ár: {sell_price:,.0f} Ft", text_color="white")
                res_prof1.configure(text=f"Tiszta haszon: {profit:,.0f} Ft", text_color="white")
            except ValueError:
                res_price1.configure(text="Hibás szám!", text_color="red")
                res_prof1.configure(text="")

        customtkinter.CTkButton(tabview.tab("Eladási ár számítás"), text="Kalkuláció", command=calc1).pack(pady=15)
        net_entry2 = customtkinter.CTkEntry(tabview.tab("Alkudozás (Visszaszámolás)"),placeholder_text="Beszerzési ár (Ft)...", width=200)
        net_entry2.pack(pady=10)

        sell_entry2 = customtkinter.CTkEntry(tabview.tab("Alkudozás (Visszaszámolás)"),placeholder_text="Kért eladási ár (Ft)...", width=200)
        sell_entry2.pack(pady=10)

        res_marg2 = customtkinter.CTkLabel(tabview.tab("Alkudozás (Visszaszámolás)"), text="Haszonkulcs: - %",font=("Arial", 16, "bold"))
        res_marg2.pack(pady=5)

        res_prof2 = customtkinter.CTkLabel(tabview.tab("Alkudozás (Visszaszámolás)"), text="Tiszta haszon: - Ft",font=("Arial", 14))
        res_prof2.pack(pady=5)

        def calc2():
            try:
                net = float(net_entry2.get())
                sell = float(sell_entry2.get())
                marg, prof = calculate_reverse_margin(net, sell)
                res_marg2.configure(text=f"Haszonkulcs: {marg:.2f} %", text_color="white")
                res_prof2.configure(text=f"Tiszta haszon: {prof:,.0f} Ft", text_color="white")
            except ValueError:
                res_marg2.configure(text="Hibás szám!", text_color="red")
                res_prof2.configure(text="")

        customtkinter.CTkButton(tabview.tab("Alkudozás (Visszaszámolás)"), text="Kalkuláció", command=calc2).pack(
            pady=15)

    else:
        open_margin_window.window.focus()
        open_margin_window.window.lift()