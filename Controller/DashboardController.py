import csv
import datetime
import math
import os.path
from tkinter import ttk, filedialog, messagebox
from fpdf import fpdf
from sqlalchemy import func

import View.PartsView as PartView
from Controller import PartsController as PartsController, TransactionController
import customtkinter

import View.CompatibilityView as CompatibilitiesView
from Controller import CompatibilityController as CompatibilitiesController
from Controller.AdminController import AdminController
from Model.database import Parts, Sessionlocal, SellItem, SellHeader, ROLE_ADMIN
from View.AdminView import AdminView
from View.TransactionView import TransactionView

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.view.export_csv_button.configure(command=self.export_inventory_csv)

        self.view.admin_button.configure(command=self.open_admin_panel)

    def clear_main_frame(self):
        for widget in self.view.main_frame.winfo_children():
            widget.destroy()
        self.view.back_button.grid(row=15, column=0, padx=20, pady=20, sticky="s")

    def show_transaction(self):
        self.clear_main_frame()
        transaction_view = TransactionView(self.view.main_frame)
        transaction_view.pack(fill="both", expand=True)
        self.transaction_controller = TransactionController.TransactionController(
            self.main_app, transaction_view)

    def logout(self):
        self.back()
        self.main_app.login.username.delete(0, "end")
        self.main_app.login.password.delete(0, "end")
        self.main_app.login.error_label.configure(text="", fg_color="transparent")
        self.main_app.login.password.configure(show="*")
        self.main_app.show_login()

    def show_parts(self):
        self.clear_main_frame()

        parts_view = PartView.PartsView(self.view.main_frame)
        parts_view.pack(fill="both", expand=True)
        parts_controller = PartsController.PartsController(self.main_app, parts_view)

    def back(self):
        self.clear_main_frame()
        self.view.back_button.grid_remove()
        self.view.welcome_label = customtkinter.CTkLabel(self.view.main_frame, text="Vezetői Műszerfal",font=customtkinter.CTkFont(size=24, weight="bold"))
        self.view.welcome_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.view.stats_frame = customtkinter.CTkFrame(self.view.main_frame, fg_color="transparent")
        self.view.stats_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.view.stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.view.card1 = customtkinter.CTkFrame(self.view.stats_frame, corner_radius=10, fg_color="#1f538d")
        self.view.card1.grid(row=0, column=0, padx=10, sticky="ew")
        self.view.card1_title = customtkinter.CTkLabel(self.view.card1, text="Nyilvántartott Alkatrészek", text_color="white", font=customtkinter.CTkFont(size=14))
        self.view.card1_title.pack(pady=(15, 0))
        self.view.card1_value = customtkinter.CTkLabel(self.view.card1, text="- db", text_color="white", font=customtkinter.CTkFont(size=26, weight="bold"))
        self.view.card1_value.pack(pady=(0, 15))

        self.view.card2 = customtkinter.CTkFrame(self.view.stats_frame, corner_radius=10, fg_color="#166534")
        self.view.card2.grid(row=0, column=1, padx=10, sticky="ew")
        self.view.card2_title = customtkinter.CTkLabel(self.view.card2, text="Raktárkészlet Értéke", text_color="white", font=customtkinter.CTkFont(size=14))
        self.view.card2_title.pack(pady=(15, 0))
        self.view.card2_value = customtkinter.CTkLabel(self.view.card2, text="- Ft", text_color="white", font=customtkinter.CTkFont(size=26, weight="bold"))
        self.view.card2_value.pack(pady=(0, 15))

        self.view.card3 = customtkinter.CTkFrame(self.view.stats_frame, corner_radius=10, fg_color="#991b1b")
        self.view.card3.grid(row=0, column=2, padx=10, sticky="ew")
        self.view.card3_title = customtkinter.CTkLabel(self.view.card3, text="Kritikus Készletszinten", text_color="white", font=customtkinter.CTkFont(size=14))
        self.view.card3_title.pack(pady=(15, 0))
        self.view.card3_value = customtkinter.CTkLabel(self.view.card3, text="- db", text_color="white", font=customtkinter.CTkFont(size=26, weight="bold"))
        self.view.card3_value.pack(pady=(0, 15))

        self.view.chart_frame = customtkinter.CTkFrame(self.view.main_frame, corner_radius=10, fg_color="gray20")
        self.view.chart_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        self.load_dashboard_stats()

    def show_compatibility(self):
        user = self.main_app.current_user
        if user is None or user.role_id != ROLE_ADMIN:
            messagebox.showerror("Hiba", "Ehhez nincs jogosultságod!")
            return
        self.clear_main_frame()
        compatibility_view = CompatibilitiesView.CompatibilityView(self.view.main_frame)
        compatibility_view.pack(fill="both", expand=True)
        compatibility_controller = CompatibilitiesController.CompatibilityController(self.main_app, compatibility_view)

    def check_inventory_alerts(self):
        missing_parts = self.low_stock()
        if missing_parts:
            self.show_low_stock_popup(missing_parts)
        self.load_dashboard_stats()

    def low_stock(self):
        with Sessionlocal() as session:
            try:
                since = datetime.datetime.now() - datetime.timedelta(days=90)
                sold = dict(
                    session.query(SellItem.part_id, func.sum(SellItem.amount))
                    .join(SellHeader)
                    .filter(SellHeader.date >= since)
                    .group_by(SellItem.part_id)
                    .all()
                )
                result = []
                for part in session.query(Parts).all():
                    per_day = (sold.get(part.id) or 0) / 90
                    min_level = max(part.min_amount, math.ceil(per_day * 7))
                    if part.amount < min_level:
                        target = max(part.max_amount, math.ceil(per_day * 13))
                        result.append((part.part_number, part.name, part.amount,
                                       max(target - part.amount, 0)))
                return result

            except Exception as e:
                session.rollback()
                print("Sikertelen adatlekérés!", e)
                return []

    def load_dashboard_stats(self):
        if not hasattr(self.view, "card1_value"):
            return

        with Sessionlocal() as session:
            try:
                all_parts = session.query(Parts).all()

                total_parts_count = sum(p.amount for p in all_parts)
                total_value = sum(p.amount * p.price for p in all_parts)
                critical_count = len(self.low_stock() or [])

                self.view.card1_value.configure(text=f"{total_parts_count} db")
                self.view.card2_value.configure(text=f"{total_value:,.0f} Ft".replace(",", " "))
                self.view.card3_value.configure(text=f"{critical_count} db")

                category_data = {}
                for part in all_parts:
                    if part.amount > 0:
                        cat = part.type if part.type else "Egyéb"
                        category_data[cat] = category_data.get(cat, 0) + part.amount

                for widget in self.view.chart_frame.winfo_children():
                    widget.destroy()

                if category_data:
                    self.draw_chart(category_data)
                else:
                    empty_label = customtkinter.CTkLabel(self.view.chart_frame, text="Nincs elég adat a grafikonhoz",
                                                         text_color="gray")
                    empty_label.pack(expand=True)

            except Exception as e:
                print(f"Hiba a statisztikák betöltésekor: {e}")

    def draw_chart(self, category_data):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')

        labels = list(category_data.keys())
        sizes = list(category_data.values())

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            textprops=dict(color="w", fontsize=10),
            colors=plt.cm.Set3.colors
        )

        centre_circle = plt.Circle((0, 0), 0.70, fc='#333333')
        fig.gca().add_artist(centre_circle)

        ax.axis('equal')
        plt.title('Raktárkészlet eloszlása kategóriánként', color='white', pad=20, fontsize=14, fontweight='bold')

        canvas = FigureCanvasTkAgg(fig, master=self.view.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

        plt.close(fig)

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

            pdf.add_font("Arial", "", "assets/fonts/arial.ttf")
            pdf.add_font("Arial", "B", "assets/fonts/arialbd.ttf")
            pdf.add_font("Arial", "I", "assets/fonts/ariali.ttf")

            pdf.set_font("Arial", style="B", size=16)
            current_date = datetime.datetime.now().strftime("%Y.%m.%d")
            pdf.cell(0,10, text='Raktárkészlet', align="center", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Arial", size=10)
            pdf.cell(0,10, text=f"Lekérdezés dátuma: {current_date}", align="center",new_x="LMARGIN", new_y="NEXT")

            pdf.ln(5)
            pdf.set_font("Arial", style="B", size=10)
            pdf.cell(35,10, "Cikkszám", border=1, align="center")
            pdf.cell(20,10,"Kép", border=1, align="center")
            pdf.cell(75,10, "Megnevezés", border=1, align="center")
            pdf.cell(30,10, "Készlet", border=1, align="center")
            pdf.cell(30,10, "Egység ár", border=1, align="center",new_x="LMARGIN", new_y="NEXT")

            pdf.set_font("Arial", size=10)
            for part in parts:
                if part.name:
                    safe_name = part.name[:45]
                else:
                    safe_name = "Ismeretlen"
                if part.part_number:
                    safe_part_num = part.part_number[:20]
                else:
                    safe_part_num = "N/A"
                row_height = 20

                pdf.cell(35, row_height, safe_part_num, border=1, align='C')
                img_x = pdf.get_x()
                img_y = pdf.get_y()
                pdf.cell(20,row_height, "", border=1)

                if part.image_path and os.path.exists(part.image_path):
                    pdf.image(part.image_path, x=img_x+2, y=img_y+2, w=16)
                else:
                    pdf.text(img_x+9,img_y+11, "-")
                pdf.cell(75, row_height, safe_name, border=1, align='L')
                pdf.cell(30, row_height, f"{part.amount} db", border=1, align='C')
                pdf.cell(30, row_height, f"{part.price} Ft", border=1, new_x="LMARGIN", new_y="NEXT", align='R')

            pdf.output(filepath)
            messagebox.showinfo("Siker","A raktárkészlet PDF sikeresen elmentve!")

        except Exception as e:
            print(f"Hiba a PDF generálásakor: {e}")
            messagebox.showerror("Hiba", "Nem sikerült legenerálni a PDF-et.")

    def export_inventory_csv(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV fájlok", "*.csv"), ("Minden fájl", "*.*")],
            title="Leltárív exportálása Excelbe"
        )

        if not filepath:
            return

        with Sessionlocal() as session:
            try:
                parts = session.query(Parts).all()
                with open(filepath, mode='w', newline='', encoding='cp1250') as file:
                    file.write("sep=;\n")
                    writer = csv.writer(file, delimiter=';')

                    writer.writerow(
                        ["Cikkszám", "Megnevezés", "Típus", "Készlet (db)", "Egységár (Ft)", "Összérték (Ft)"])

                    for part in parts:
                        if part.part_number:
                            safe_part_num = part.part_number
                        else:
                            safe_part_num = "-"
                        if part.name:
                            safe_name = part.name
                        else:
                            safe_name = "Ismeretlen"
                        if part.type:
                            safe_type = part.type
                        else:
                            safe_type = "-"
                        total_value = part.amount * part.price

                        writer.writerow([safe_part_num, safe_name, safe_type, part.amount, part.price, total_value])

                messagebox.showinfo("Siker", "A leltárív sikeresen exportálva CSV formátumban!")
            except Exception as e:
                print(f"Hiba a CSV exportálásakor: {e}")
                messagebox.showerror("Hiba", "Nem sikerült exportálni az adatokat.")

    def show_low_stock_popup(self, low_part):
        popup = customtkinter.CTkToplevel()
        popup.title("Kevés az alkatrész!")
        popup.geometry("620x450")
        popup_label = customtkinter.CTkLabel(popup, text="Alkatrészek:")
        popup_label.pack(pady=10)

        table_frame = customtkinter.CTkFrame(popup)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ["part_number", "name", "amount", "for_order"]
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0, rowheight=25)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#343638')])
        parts_tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")
        parts_tree.heading("part_number", text="Cikkszám")
        parts_tree.heading("name", text="Megnevezés")
        parts_tree.heading("amount", text="Mennyiség")
        parts_tree.heading("for_order", text="Rendelési javaslat")
        parts_tree.column("part_number", width=120, anchor="center")
        parts_tree.column("name", width=220, anchor="w")
        parts_tree.column("amount", width=90, anchor="center")
        parts_tree.column("for_order", width=140, anchor="center")

        parts_tree.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        parts_tree.scrollbar = customtkinter.CTkScrollbar(table_frame, command=parts_tree.yview)
        parts_tree.scrollbar.grid(row=0, column=1, sticky="ns")
        parts_tree.configure(yscrollcommand=parts_tree.scrollbar.set)

        button_frame = customtkinter.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=(5, 20))

        popup_continue_button = customtkinter.CTkButton(button_frame, text="Folytatás a raktárhoz", command=lambda: self.option_continue(popup))
        popup_continue_button.grid(row=0, column=0, padx=10)

        popup_cancel_button = customtkinter.CTkButton(button_frame, text="Bezárás", fg_color="gray40",hover_color="gray30", command=popup.destroy)
        popup_cancel_button.grid(row=0, column=1, padx=10)
        for part_number, name, amount, order in low_part:
            parts_tree.insert("", "end", values=(part_number, name, amount, order))

    def open_admin_panel(self):
        user = self.main_app.current_user
        if user is None or user.role_id != ROLE_ADMIN:
            messagebox.showerror("Hiba", "Ehhez nincs jogosultságod!")
            return
        self.clear_main_frame()
        admin_view = AdminView(self.view.main_frame)
        admin_view.pack(fill="both", expand=True)
        self.admin_controller = AdminController(self.main_app, admin_view)