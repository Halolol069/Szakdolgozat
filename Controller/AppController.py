from pathlib import Path

import View.MainView as MainView
import View.LoginView as LoginView
import View.RegisterView as RegisterView
import View.DashboardView as DashboardView
import Controller.RegisterController as RegisterController
import Controller.LoginController as LoginController
import Controller.DashboardController as DashboardController
from Model.database import ROLE_ADMIN
import importlib

class Controller:
    def __init__(self):
        self.current_user = None
        self.app = MainView.MainView()
        self.login = LoginView.LoginView(self.app)
        self.register = RegisterView.RegisterView(self.app)
        self.dashboard = DashboardView.DashboardView(self.app)
        self.register_controller = RegisterController.RegisterController(self,self.register)
        self.login_controller = LoginController.LoginController(self,self.login)
        self.dashboard_controller = DashboardController.DashboardController(self, self.dashboard)
        self.login.register_button.configure(command=self.show_register)
        self.app.show_frame(self.login)
        self.load_plugins()

        self.app.mainloop()
    def show_register(self):
        self.app.show_frame(self.register)

    def show_login(self):
        self.current_user = None
        self.app.show_frame(self.login)

    def show_dashboard(self):
        if self.current_user is None:
            self.show_login()
            return
        self.app.show_frame(self.dashboard)
        if self.current_user.role_id == ROLE_ADMIN:
            self.dashboard.compatibility_button.grid(row=3, column=0, padx=20, pady=10)
        else:
            self.dashboard.compatibility_button.grid_forget()

    def load_plugins(self):
        plugin_folder = Path(__file__).parent / "plugins"
        plugin_folder.mkdir(exist_ok=True)

        for file in sorted(plugin_folder.glob("*.py")):
            if file.name.startswith("__"):
                continue
            try:
                module = importlib.import_module(f"Controller.plugins.{file.stem}")
                if hasattr(module, "register"):
                    module.register(self)
                else:
                    print(f"A(z) {file.stem} nem tartalmazza a 'register' függvényt.")
            except Exception as e:
                print(f"Nem sikerült betölteni a {file.stem} plugint: {e}")



if __name__ == '__main__':
    controller = Controller()