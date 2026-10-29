import customtkinter

class MainView(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.current_frame = None
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.state("zoomed")
    def show_frame(self, view):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        self.current_frame = view
        self.current_frame.pack(fill="both", expand=True)