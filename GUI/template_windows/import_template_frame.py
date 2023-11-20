import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

class ImportTemplateWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Import Vorlage")
        self.geometry("700x200")

        # Label zur Anzeige der Importanweisungen
        self.label = ctk.CTkLabel(self, text="Wählen Sie die zu importierende Vorlage aus:", text_color="white")
        self.label.pack(pady=10)

        # Button zur Auswahl der zu importierenden Datei (links)
        self.choose_file_button = ctk.CTkButton(self, text="Datei auswählen", command=self.choose_file)
        self.choose_file_button.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        # Eingabefeld für den Dateipfad, für Benutzereingaben deaktiviert (rechts)
        self.dateipfad_eingabe = ctk.CTkEntry(self, width=600, state='disabled', placeholder_text="VAR_DATEIPFAD")
        self.dateipfad_eingabe.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Buttons für Abbrechen und Importieren
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.destroy)
        self.cancel_button.place(relx=0.3, rely=0.8, anchor=ctk.CENTER)

        self.import_button = ctk.CTkButton(self, text="Importieren", command=self.import_template)
        self.import_button.place(relx=0.7, rely=0.8, anchor=ctk.CENTER)

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
        # Hier können Sie den ausgewählten Pfad verwenden, um die Vorlage zu importieren
        if self.selected_path:
            # Importieren Sie die Vorlage von dem ausgewählten Pfad
            # Fügen Sie Ihren Code zum Importieren der Vorlage hier ein
            print(f"Vorlage von {self.selected_path} wurde erfolgreich importiert.")
            self.destroy()
        else:
            # Zeigen Sie eine Fehlermeldung an, wenn keine Datei ausgewählt wurde
            ctk.CTkMessageBox.showerror("Fehler", "Bitte wählen Sie eine Datei zum Importieren aus.")

if __name__ == "__main__":
    # Erstellen Sie das ImportTemplateWindow
    import_window = ImportTemplateWindow()
    import_window.mainloop()
