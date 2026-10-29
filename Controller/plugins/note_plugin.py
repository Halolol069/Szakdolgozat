import customtkinter
import os

def register(app):
    print("Gyors jegyzet indítása!")

    try:
        target_frame = app.dashboard.sidebar_frame
    except AttributeError:
        target_frame=app.dashboard

    plugin_button = customtkinter.CTkButton(
        master=target_frame,
        text="Gyors jegyzet",
        fg_color="green",
        hover_color="red",
        command=open_notes
    )
    plugin_button.grid(row=9, column=0, padx=20, pady=10)

def read_notes_file(filepath="note.txt"):
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def write_note_file(content: str, filepath="note.txt"):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def open_notes():
    window=customtkinter.CTkToplevel()
    window.title("Gyors jegyzet")
    window.geometry("500x500")
    window.attributes("-topmost", True)

    title_label= customtkinter.CTkLabel(window, text="Napi emlékeztetők!", font=("Arial", 16, "bold"))
    title_label.pack(pady=15)

    textbox = customtkinter.CTkTextbox(window, width=350, height=250)
    textbox.pack(pady=10)

    existing_notes = read_notes_file()
    if existing_notes:
        textbox.insert("1.0", existing_notes)

    def save_note():
        sentences = textbox.get("1.0", "end")

        write_note_file(sentences)

        save_button.configure(text="Sikeres mentés!", fg_color="green")

        window.after(2000, lambda:save_button.configure(text="Mentés", fg_color="green"))

    save_button = customtkinter.CTkButton(window, text="Mentés", command=save_note)
    save_button.pack(pady=10)