import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

class ExportTemplateWindow(ctk.CTkFrame):
    def __init__(self, container, X, Y, template_name):
        self.template_name = template_name
        self.fg_color = "#242424"
        super().__init__(container,width= X,height=Y, fg_color=self.fg_color)
        self.container = container

        # Label zur Anzeige des ausgewählten Vorlagennamens
        self.label = ctk.CTkLabel(self, text=f"Wo möchten Sie die Vorlage '{self.template_name}' abspeichern?", text_color="white")
        self.label.place(relx=0.5,rely=0.3, anchor=ctk.CENTER)

        # Button zur Auswahl des Speicherorts (links)
        self.choose_path_button = ctk.CTkButton(self, text="Speicherort", command=self.choose_path)
        self.choose_path_button.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        # Eingabefeld für den Dateipfad, für Benutzereingaben deaktiviert (rechts)
        self.dateipfad_eingabe = ctk.CTkEntry(self, width=600, state='disabled', placeholder_text="VAR_DATEIPFAD")
        self.dateipfad_eingabe.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Buttons für Abbrechen, Speicherort und Speichern
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.abbrechen_template)
        self.cancel_button.place(relx=0.4, rely=0.6, anchor=ctk.CENTER)

        self.save_button = ctk.CTkButton(self, text="Speichern", command=self.save_template)
        self.save_button.place(relx=0.6, rely=0.6, anchor=ctk.CENTER)

        self.selected_template_name = self.template_name
        self.selected_path = ""


    def choose_path(self):
        # Öffnen Sie den Dateidialog mit einem Standarddateinamen, der dem selected_template_name entspricht
        self.selected_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Dateien", "*.json")], initialfile=self.selected_template_name)

        # Aktualisieren Sie die Anzeige des ausgewählten Pfads
        self.dateipfad_eingabe.configure(state='normal')
        self.dateipfad_eingabe.delete(0, tk.END)
        self.dateipfad_eingabe.insert(0, self.selected_path)
        self.dateipfad_eingabe.configure(state='disabled')

    def save_template(self):
        if self.selected_path:
            # Übergabe des Template-Namens und des Exportpfads an die Callback-Methode im Hauptfenster
            self.container.process_export_template_frame(self.template_name, self.selected_path)
    
    def abbrechen_template(self):
        self.container.export_template_abbrechen_callback()
            
if __name__ == "__main__":
    # Nehmen Sie an, dass Sie den ausgewählten Vorlagennamen bereits aus dem Hauptfenster haben
    selected_template_name = "Name der Vorlage"
    
    # Erstellen Sie das ExportTemplateWindow und übergeben Sie den ausgewählten Vorlagennamen
    export_window = ExportTemplateWindow(selected_template_name)
    export_window.mainloop()
