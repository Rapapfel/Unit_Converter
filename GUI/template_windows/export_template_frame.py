import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

class ExportTemplateWindow(ctk.CTkFrame):
    def __init__(self, container, X, Y, template_name):
        """
        Konstruktor der ExportTemplateWindow-Klasse.

        Parameter:
        - container: Tkinter-Container, in dem das Fenster platziert wird.
        - X: Breite des Fensters.
        - Y: Höhe des Fensters.
        - template_name: Name der zu exportierenden Vorlage.
        """
        self.template_name = template_name
        self.fg_color = "#242424"
        super().__init__(container, width=X, height=Y, fg_color=self.fg_color)
        self.container = container

        # Label zur Anzeige des ausgewählten Vorlagennamens
        self.label = ctk.CTkLabel(self, text=f"Wo möchten Sie die Vorlage '{self.template_name}' abspeichern?", text_color="white")
        self.label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        # Button zur Auswahl des Speicherorts
        self.choose_path_button = ctk.CTkButton(self, text="Speicherort", command=self.choose_path)
        self.choose_path_button.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        # Eingabefeld für den Dateipfad
        self.dateipfad_eingabe = ctk.CTkEntry(self, width=600, state='disabled', placeholder_text="VAR_DATEIPFAD")
        self.dateipfad_eingabe.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Buttons für Abbrechen und Speichern
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.abbrechen_template)
        self.cancel_button.place(relx=0.4, rely=0.6, anchor=ctk.CENTER)
        self.save_button = ctk.CTkButton(self, text="Speichern", command=self.save_template)
        self.save_button.place(relx=0.6, rely=0.6, anchor=ctk.CENTER)

        self.selected_template_name = self.template_name
        self.selected_path = ""

    def choose_path(self):
        """
        Öffnet einen Dateidialog zur Auswahl eines Speicherorts für die Vorlage.
        Aktualisiert das Eingabefeld 'dateipfad_eingabe' mit dem ausgewählten Pfad.
        """
        # Standarddateiname entspricht dem Namen der Vorlage
        self.selected_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Dateien", "*.json")], initialfile=self.selected_template_name)

        # Aktualisieren des Eingabefelds mit dem ausgewählten Pfad
        self.dateipfad_eingabe.configure(state='normal')
        self.dateipfad_eingabe.delete(0, tk.END)
        self.dateipfad_eingabe.insert(0, self.selected_path)
        self.dateipfad_eingabe.configure(state='disabled')

    def save_template(self):
        """
        Verarbeitet das Speichern der Vorlage.
        Ruft eine Callback-Methode im Hauptfenster auf, um den Exportprozess durchzuführen.
        """
        if self.selected_path:
            # Übergabe des Template-Namens und des Pfads an die Callback-Methode
            self.container.process_export_template_frame(self.template_name, self.selected_path)

    def abbrechen_template(self):
        """
        Verarbeitet das Abbrechen des Exportvorgangs.
        Ruft eine Callback-Methode im Hauptfenster auf, um den Vorgang abzubrechen.
        """
        self.container.export_template_abbrechen_callback()

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

    # Annahme eines ausgewählten Vorlagennamens
    selected_template_name = "Name der Vorlage"

    # Erstellung und Anzeige des ExportTemplateWindow
    export_window = ExportTemplateWindow(root, window_width, window_height, selected_template_name)
    export_window.pack(fill="both", expand=True)

    # Start des Event-Loops
    root.mainloop()
