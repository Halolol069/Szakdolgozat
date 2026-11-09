import datetime

import customtkinter
import os

def register(app):
    print("Közös üzenőfal indítása!")

    try:
        target_frame = app.dashboard.sidebar_frame
    except AttributeError:
        target_frame=app.dashboard

    plugin_button = customtkinter.CTkButton(
        master=target_frame,
        text="Közös üzenőfal",
        fg_color="green",
        hover_color="red",
        command=open_notes
    )
    plugin_button.grid(row=8, column=0, padx=20, pady=10)

def read_notes_file(filepath="note.txt"):
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def write_note_file(content: str, filepath="note.txt"):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def open_notes():
    if not hasattr(open_notes, "window") or not open_notes.window.winfo_exists():
        window=customtkinter.CTkToplevel()
        open_notes.window = window
        window.title("Közös üzenőfal")
        window.geometry("500x500")
        window.attributes("-topmost", True)

        title_label= customtkinter.CTkLabel(window, text="Napi emlékeztetők!", font=("Arial", 16, "bold"))
        title_label.pack(pady=15)

        def insert_timestamp():
            now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M] - ")
            textbox.insert("insert", now)
            textbox.focus()

        time_button = customtkinter.CTkButton(window, text="Időbélyeg (Dátum) beszúrása", fg_color="gray40",hover_color="gray30", width=150, command=insert_timestamp)
        time_button.pack(pady=(0, 10))

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
    else:
        open_notes.window.focus()
        open_notes.window.lift()