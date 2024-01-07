import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

class ImportTemplateWindow(ctk.CTkFrame):
    def __init__(self,container, X, Y):
        self.fg_color = "#242424"
        super().__init__(container,width= X,height=Y, fg_color=self.fg_color)

        self.container = container

        # Label zur Anzeige der Importanweisungen
        self.label = ctk.CTkLabel(self, text="Wählen Sie die zu importierende Vorlage aus:", text_color="white")
        self.label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        # Button zur Auswahl der zu importierenden Datei (links)
        self.choose_file_button = ctk.CTkButton(self, text="Datei auswählen", command=self.choose_file)
        self.choose_file_button.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        # Eingabefeld für den Dateipfad, für Benutzereingaben deaktiviert (rechts)
        self.dateipfad_eingabe = ctk.CTkEntry(self, width=600, state='disabled', placeholder_text="VAR_DATEIPFAD")
        self.dateipfad_eingabe.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Buttons für Abbrechen und Importieren
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.abbrechen_template)
        self.cancel_button.place(relx=0.4, rely=0.6, anchor=ctk.CENTER)

        self.import_button = ctk.CTkButton(self, text="Importieren", command=self.import_template)
        self.import_button.place(relx=0.6, rely=0.6, anchor=ctk.CENTER)

        self.selected_path = ""

    def choose_file(self):
        # Öffnen Sie den Dateidialog, um die Datei zum Importieren auszuwählen
        self.selected_path = filedialog.askopenfilename(filetypes=[("JSON Dateien", "*.json")])

        # Aktualisieren Sie die Anzeige des ausgewählten Pfads
        self.dateipfad_eingabe.configure(state='normal')
        self.dateipfad_eingabe.delete(0, tk.END)
        self.dateipfad_eingabe.insert(0, self.selected_path)
        self.dateipfad_eingabe.configure(state='disabled')

    def import_template(self):
        if self.selected_path:
            self.container.process_import_template_frame(self.selected_path)
    
    def abbrechen_template(self):
        self.container.import_template_abbrechen_callback()


if __name__ == "__main__":
    # Erstellen eines Hauptfensters
    root = ctk.CTk()

    # Konfiguration der Fenstergröße und Position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = screen_width // 2
    window_height = screen_height // 2
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Instanziieren und Anzeigen des ImportTemplateWindow
    import_window = ImportTemplateWindow(root, window_width, window_height)
    import_window.pack(fill="both", expand=True)

    # Starten des Event-Loops
    root.mainloop()
