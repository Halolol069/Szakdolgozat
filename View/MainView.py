import customtkinter

class MainView(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.current_frame = None
        self.geometry("600x600")
    def show_frame(self, view):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        self.current_frame = view
        self.current_frame.pack(fill="both", expand=True)




