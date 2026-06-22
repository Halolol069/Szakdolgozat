import View.PartsView as PartView
import PartsController as PartsController

class DashboardController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view

        self.view.logout_button.configure(command=self.logout)

        self.view.parts_button.configure(command=self.show_parts)

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