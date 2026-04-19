import customtkinter

class MainView(customtkinter.CTk):
    def __init__(self, master, values):
        super().__init__(master)
        self.values = values

