from View.AddPartView import AddPartView


class PartsController:
    def __init__(self, main_app, view):
        self.main_app = main_app
        self.view = view

        self.view.add_button.configure(command=self.open_add_popup)

    def open_add_popup(self):
        self.add_view = AddPartView(self.view)