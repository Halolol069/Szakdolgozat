class DashboardController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view

        self.view.logout_button.configure(command=self.logout)

    def logout(self):
        self.main_app.login.username.delete(0, "end")
        self.main_app.login.password.delete(0, "end")
        self.main_app.login.error_label.configure(text="")
        self.main_app.login.registration_label.configure(text="")
        self.main_app.show_login()