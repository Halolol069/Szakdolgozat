import View.PartsView as PartView
import PartsController as PartsController
import customtkinter

class DashboardController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view

        self.view.logout_button.configure(command=self.logout)

        self.view.parts_button.configure(command=self.show_parts)

        self.view.back_button.configure(command=self.back)

    def logout(self):
        self.main_app.login.username.delete(0, "end")
        self.main_app.login.password.delete(0, "end")
        self.main_app.login.error_label.configure(text="")
        self.main_app.login.registration_label.configure(text="")
        self.main_app.show_login()

    def show_parts(self):
        for widget in self.view.main_frame.winfo_children():
            widget.destroy()

        parts_view = PartView.PartsView(self.view.main_frame)
        parts_view.pack(fill="both", expand=True)
        parts_controller = PartsController.PartsController(self.main_app, parts_view)
        self.view.back_button.grid(row=6, column=0, padx=20, pady=20, sticky="s")

    def back(self):
        for widget in self.view.main_frame.winfo_children():
            widget.destroy()
        self.view.welcome_label = customtkinter.CTkLabel(self.view.main_frame, text="Üdvözöllek a Rendszerben!",
                                                    font=customtkinter.CTkFont(size=24, weight="bold"))
        self.view.welcome_label.pack(pady=50)
        self.view.back_button.grid_remove()

