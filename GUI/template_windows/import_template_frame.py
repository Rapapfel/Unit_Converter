import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

class ImportTemplateWindow(ctk.CTkFrame):
    """
    Klasse zur Erstellung eines Fensters für den Import von Vorlagen.

    Attribute:
    - fg_color: Vordergrundfarbe des Fensters.
    - container: Übergeordnetes Tkinter-Container-Objekt.
    """
    def __init__(self, container, X, Y):
        """
        Konstruktor der ImportTemplateWindow-Klasse.

        Parameter:
        - container: Tkinter-Container, in dem das Fenster platziert wird.
        - X: Breite des Fensters.
        - Y: Höhe des Fensters.
        """
        self.fg_color = "#242424"
        super().__init__(container, width=X, height=Y, fg_color=self.fg_color)
        self.container = container

        # Label zur Anzeige der Importanweisungen
        self.label = ctk.CTkLabel(self, text="Wählen Sie die zu importierende Vorlage aus:", text_color="white")
        self.label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        # Button zur Auswahl der zu importierenden Datei
        self.choose_file_button = ctk.CTkButton(self, text="Datei auswählen", command=self.choose_file)
        self.choose_file_button.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        # Eingabefeld für den Dateipfad
        self.dateipfad_eingabe = ctk.CTkEntry(self, width=600, state='disabled', placeholder_text="VAR_DATEIPFAD")
        self.dateipfad_eingabe.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Buttons für Abbrechen und Importieren
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.abbrechen_template)
        self.cancel_button.place(relx=0.4, rely=0.6, anchor=ctk.CENTER)
        self.import_button = ctk.CTkButton(self, text="Importieren", command=self.import_template)
        self.import_button.place(relx=0.6, rely=0.6, anchor=ctk.CENTER)

        self.selected_path = ""

    def choose_file(self):
        """
        Öffnet einen Dateidialog zur Auswahl einer Datei für den Import.
        Aktualisiert das Eingabefeld 'dateipfad_eingabe' mit dem ausgewählten Pfad.
        """
        # Dateidialog zum Auswählen der Importdatei
        self.selected_path = filedialog.askopenfilename(filetypes=[("JSON Dateien", "*.json")])

        # Aktualisieren des Eingabefelds mit dem ausgewählten Pfad
        self.dateipfad_eingabe.configure(state='normal')
        self.dateipfad_eingabe.delete(0, tk.END)
        self.dateipfad_eingabe.insert(0, self.selected_path)
        self.dateipfad_eingabe.configure(state='disabled')

    def import_template(self):
        """
        Verarbeitet das Importieren der Vorlage.
        Ruft eine Callback-Methode im Hauptfenster auf, um den Importprozess durchzuführen.
        """
        if self.selected_path:
            # Übergabe des Pfads an die Callback-Methode
            self.container.process_import_template_frame(self.selected_path)

    def abbrechen_template(self):
        """
        Verarbeitet das Abbrechen des Importvorgangs.
        Ruft eine Callback-Methode im Hauptfenster auf, um den Vorgang abzubrechen.
        """
        self.container.import_template_abbrechen_callback()

# Hauptfenster-Erstellung und -Konfiguration
if __name__ == "__main__":
    root = ctk.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = (3 * screen_width) // 4
    window_height = (2 * screen_height) // 3
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Erstellung und Anzeige des ImportTemplateWindow
    import_window = ImportTemplateWindow(root, window_width, window_height)
    import_window.pack(fill="both", expand=True)

    # Start des Event-Loops
    root.mainloop()
