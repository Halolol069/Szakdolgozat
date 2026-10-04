import datetime
from tkinter import ttk, filedialog, messagebox
from fpdf import fpdf

import View.PartsView as PartView
from Controller import PartsController as PartsController, TransactionController
import customtkinter

import View.CompatibilityView as CompatibilitiesView
from Controller import CompatibilityController as CompatibilitiesController
from Model.database import Parts, Sessionlocal, TransactionLog
from View.TransactionView import TransactionView


class DashboardController:

    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view

        self.view.logout_button.configure(command=self.logout)

        self.view.parts_button.configure(command=self.show_parts)

        self.view.compatibility_button.configure(command=self.show_compatibility)

        self.view.back_button.configure(command=self.back)

        self.view.transaction_button.configure(command=self.show_transaction)

        self.view.export_pdf_button.configure(command=self.export_inventory_pdf)

    def clear_main_frame(self):
        for widget in self.view.main_frame.winfo_children():
            widget.destroy()
        self.view.back_button.grid(row=6, column=0, padx=20, pady=20, sticky="s")

    def show_transaction(self):
        self.clear_main_frame()
        transaction_view = TransactionView(self.view.main_frame)
        transaction_view.pack(fill="both", expand=True)
        self.transaction_controller = TransactionController.TransactionController(
            self.main_app, transaction_view)

    def logout(self):
        self.main_app.login.username.delete(0, "end")
        self.main_app.login.password.delete(0, "end")
        self.main_app.login.error_label.configure(text="")
        self.main_app.login.registration_label.configure(text="")
        self.main_app.show_login()

    def show_parts(self):
        self.clear_main_frame()

        parts_view = PartView.PartsView(self.view.main_frame)
        parts_view.pack(fill="both", expand=True)
        parts_controller = PartsController.PartsController(self.main_app, parts_view)

    def back(self):
        for widget in self.view.main_frame.winfo_children():
            widget.destroy()
        self.view.welcome_label = customtkinter.CTkLabel(self.view.main_frame, text="Üdvözöllek a Rendszerben!",
                                                    font=customtkinter.CTkFont(size=24, weight="bold"))
        self.view.welcome_label.pack(pady=50)
        self.view.back_button.grid_remove()

    def show_compatibility(self):
        self.clear_main_frame()
        compatibility_view = CompatibilitiesView.CompatibilityView(self.view.main_frame)
        compatibility_view.pack(fill="both", expand=True)
        compatibility_controller = CompatibilitiesController.CompatibilityController(self.main_app, compatibility_view)

    def check_inventory_alerts(self):
        missing_parts = self.low_stock()
        if missing_parts:
            self.show_low_stock_popup(missing_parts)

    def low_stock(self):
        with Sessionlocal() as session:
            try:
                low_part_list = session.query(Parts).filter(Parts.amount < Parts.min_amount).all()
                if len(low_part_list) > 0:
                    return low_part_list
            except Exception as e:
                print("Sikertelen az adat lekérés", e)

    def option_continue(self, popup):
        popup.destroy()
        self.show_parts()

    def export_inventory_pdf(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF fájlok", "*.pdf")],
            title="PDF export"
        )

        if not filepath:
            return

        try:
            with Sessionlocal() as session:
                parts =session.query(Parts).all()

            pdf = fpdf.FPDF()
            pdf.add_page()

            pdf.set_font("Helvetica", style="B", size=16)
            current_date = datetime.datetime.now().strftime("%Y.%m.%d")
            pdf.cell(0,10, text='Raktárkészlet', align="center", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", size=10)
            pdf.cell(0,10, text=f"Lekérdezés dátuma: {current_date}", align="center",new_x="LMARGIN", new_y="NEXT")

            pdf.ln(5)
            pdf.set_font("Helvetica", style="B", size=10)
            pdf.cell(40,10, "Cikkszám", border=1, align="center")
            pdf.cell(90,10, "Megnevezés", border=1, align="center")
            pdf.cell(30,10, "Készlet", border=1, align="center")
            pdf.cell(30,10, "Egység ár", border=1, align="center",new_x="LMARGIN", new_y="NEXT")

            pdf.set_font("Helvetica", size=10)
            for part in parts:
                if part.name:
                    safe_name = part.name[45:]
                else:
                    print("Ismeretlen")
                if part.part_number:
                    safe_part_num = part.part_number[:20]
                else:
                    "N/A"

                pdf.cell(40, 10, safe_part_num, border=1, align='C')
                pdf.cell(90, 10, safe_name, border=1, align='L')
                pdf.cell(30, 10, f"{part.amount} db", border=1, align='C')
                pdf.cell(30, 10, f"{part.price} Ft", border=1, new_x="LMARGIN", new_y="NEXT", align='R')

            pdf.output(filepath)

        except Exception as e:
            print(f"Hiba a PDF generálásakor: {e}")
            messagebox.showerror("Hiba", "Nem sikerült legenerálni a PDF-et.")


    def show_low_stock_popup(self, low_part):
        popup = customtkinter.CTkToplevel()
        popup.title("Kevés az alkatrész!")
        popup.geometry("500x400")
        popup_label = customtkinter.CTkLabel(popup, text="Alkatrészek:")
        popup_label.pack(pady=10)

        table_frame = customtkinter.CTkFrame(popup)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ["part_number", "name", "amount", "for_order"]
        parts_tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")
        parts_tree.heading("part_number", text="Cikkszám")
        parts_tree.heading("name", text="Megnevezés")
        parts_tree.heading("amount", text="Mennyiség")
        parts_tree.heading("for_order", text="Rendelési javaslat")
        parts_tree.column("part_number", width=100, anchor="center")
        parts_tree.column("name", width=100, anchor="center")
        parts_tree.column("amount", width=80, anchor="center")
        parts_tree.column("for_order", width=120, anchor="center")

        parts_tree.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

        parts_tree.scrollbar = customtkinter.CTkScrollbar(table_frame, command=parts_tree.yview)
        parts_tree.scrollbar.grid(row=0, column=1, sticky="ns")
        parts_tree.configure(yscrollcommand=parts_tree.scrollbar.set)

        popup_continue_button = customtkinter.CTkButton(popup, text="Folytatás", command=lambda : self.option_continue(popup))
        popup_continue_button.pack(pady=10)

        popup_cancel_button = customtkinter.CTkButton(popup, text="Kilépés", command=popup.destroy)
        popup_cancel_button.pack(pady=10)
        for parts in low_part:
            suggested_order = parts.max_amount - parts.amount
            if suggested_order < 0:
                suggested_order = 0
            parts_tree.insert("", "end", values=(parts.part_number, parts.name, parts.amount, suggested_order), tags="part")