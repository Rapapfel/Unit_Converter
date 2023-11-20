import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

class ExportTemplateWindow(ctk.CTk):
    def __init__(self, selected_template_name):
        super().__init__()
        self.title("Export Vorlage")
        self.geometry("700x200")

        # Label zur Anzeige des ausgewählten Vorlagennamens
        self.label = ctk.CTkLabel(self, text=f"Wo möchten Sie die Vorlage '{selected_template_name}' abspeichern?", text_color="white")
        self.label.pack(pady=10)

        # Button zur Auswahl des Speicherorts (links)
        self.choose_path_button = ctk.CTkButton(self, text="Speicherort", command=self.choose_path)
        self.choose_path_button.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        # Eingabefeld für den Dateipfad, für Benutzereingaben deaktiviert (rechts)
        self.dateipfad_eingabe = ctk.CTkEntry(self, width=600, state='disabled', placeholder_text="VAR_DATEIPFAD")
        self.dateipfad_eingabe.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Buttons für Abbrechen, Speicherort und Speichern
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.destroy)
        self.cancel_button.place(relx=0.3, rely=0.8, anchor=ctk.CENTER)

        self.save_button = ctk.CTkButton(self, text="Speichern", command=self.save_template)
        self.save_button.place(relx=0.7, rely=0.8, anchor=ctk.CENTER)

        self.selected_template_name = selected_template_name
        self.selected_path = ""

    def choose_path(self):
        # Öffnen Sie den Dateidialog, um den Speicherort auszuwählen
        self.selected_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Dateien", "*.json")])

        # Aktualisieren Sie die Anzeige des ausgewählten Pfads
        self.dateipfad_eingabe.configure(state='normal')
        self.dateipfad_eingabe.delete(0, tk.END)
        self.dateipfad_eingabe.insert(0, self.selected_path)
        self.dateipfad_eingabe.configure(state='disabled')

    def save_template(self):
        # Hier können Sie den ausgewählten Pfad und den ausgewählten Vorlagennamen verwenden, um die Vorlage zu speichern
        if self.selected_path:
            # Speichern Sie die Vorlage an dem ausgewählten Pfad
            # Fügen Sie Ihren Code zum Speichern der Vorlage hier ein
            print(f"Vorlage '{self.selected_template_name}' wurde an {self.selected_path} gespeichert.")
            self.destroy()
        else:
            # Zeigen Sie eine Fehlermeldung an, wenn kein Pfad ausgewählt wurde
            ctk.CTkMessageBox.showerror("Fehler", "Bitte wählen Sie einen Speicherort für die Vorlage aus.")

if __name__ == "__main__":
    # Nehmen Sie an, dass Sie den ausgewählten Vorlagennamen bereits aus dem Hauptfenster haben
    selected_template_name = "Name der Vorlage"
    
    # Erstellen Sie das ExportTemplateWindow und übergeben Sie den ausgewählten Vorlagennamen
    export_window = ExportTemplateWindow(selected_template_name)
    export_window.mainloop()
