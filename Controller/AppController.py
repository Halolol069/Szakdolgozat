import  View.MainView as MainView
import View.LoginView as LoginView
import View.RegisterView as RegisterView
import View.CompatibilityView as CompatibilityView
from Controller import RegisterController as RegisterController
from Controller import LoginController as LoginController
from Controller import CompatibilityController as CompatibilityController
from Controller import DashboardController
from View import DashboardView


class Controller:
    def __init__(self):
        self.app = MainView.MainView()
        self.login = LoginView.LoginView(self.app)
        self.register = RegisterView.RegisterView(self.app)
        self.dashboard = DashboardView.DashboardView(self.app)
        self.compatibility = CompatibilityView.CompatibilityView(self.app)
        self.register_controller = RegisterController.RegisterController(self,self.register)
        self.login_controller = LoginController.LoginController(self,self.login)
        self.compatibility_controller = CompatibilityController.CompatibilityController(self,self.compatibility)
        self.dashboard_controller = DashboardController.DashboardController(self, self.dashboard)
        self.login.register_button.configure(command=self.show_register)

        self.app.show_frame(self.login)
        self.app.mainloop()
    def show_register(self):
        self.app.show_frame(self.register)

    def show_login(self):
        self.app.show_frame(self.login)

    def show_compatibility(self):
        self.app.show_frame(self.compatibility)

    def show_dashboard(self):
        self.app.show_frame(self.dashboard)

if __name__ == '__main__':
    controller = Controller()

