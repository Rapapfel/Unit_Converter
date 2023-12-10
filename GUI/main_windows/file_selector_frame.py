import customtkinter as ctk
from tkinter import filedialog

class file_selector_frame(ctk.CTkFrame):
    def __init__(self, container):
        self.fg_color = "#242424"
        super().__init__(container,width=1200,height=365, fg_color=self.fg_color)
        self.selected_file_path = None  # Initialisieren Sie die Variable mit None
        self.container = container

        self.widgets_erstellen()


    def widgets_erstellen(self):
        # Beschriftung
        self.beschriftung = ctk.CTkLabel(self, text="Bitte wählen Sie den Dateipfad der IFC-Datei, bei der Sie die Einheiten ändern möchten")
        self.beschriftung.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
        
        # Schaltfläche, um abzubrechen und die Anwendung zu schließen (Links)
        self.abbrechen_schaltflaeche = ctk.CTkButton(self, text="Abbrechen", command=self.anwendung_schliessen)
        self.abbrechen_schaltflaeche.place(relx=0.3, rely=0.6, anchor=ctk.CENTER)
        
        # Schaltfläche, um den Dateipfad auszuwählen (Mitte)
        self.waehlen_schaltflaeche = ctk.CTkButton(self, text="Wählen", command=self.datei_auswaehlen)
        self.waehlen_schaltflaeche.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        
        # Schaltfläche, um zum nächsten Schritt fortzufahren (Rechts)
        self.weiter_schaltflaeche = ctk.CTkButton(self, text="Weiter", command=self.weiter_aktion)
        self.weiter_schaltflaeche.place(relx=0.7, rely=0.6, anchor=ctk.CENTER)

        # Eingabefeld für den Dateipfad, für Benutzereingaben deaktiviert
        self.dateipfad_eingabe = ctk.CTkEntry(self, width=1100, state='disabled', placeholder_text="VAR_DATEIPFAD", justify= "center")
        self.dateipfad_eingabe.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

    def datei_auswaehlen(self):
        # Einen Datei-Dialog öffnen, um eine Datei mit der Erweiterung ".ifc" auszuwählen und den Pfad im Eingabefeld anzeigen
        filetypes = [("IFC-Dateien", "*.ifc")]
        dateipfad = filedialog.askopenfilename(filetypes=filetypes)
        if dateipfad:
            self.selected_file_path = dateipfad  # Speichern des Pfades als Attribut der Klasse
            self.dateipfad_eingabe.configure(state='normal')  # Aktiviert das Eingabefeld, um den Text zu ändern
            self.dateipfad_eingabe.delete(0, ctk.END)
            self.dateipfad_eingabe.insert(0, dateipfad)
            self.dateipfad_eingabe.configure(state='disabled')  # Deaktiviert das Eingabefeld wieder

    def weiter_aktion(self):
        if self.selected_file_path:
            self.container.ifc_import_callback(self.selected_file_path)

        

    def anwendung_schliessen(self):
        # Die Anwendung schließen
        self.container.abbrechen()

if __name__ == "__main__":
    app = file_selector_frame()
    app.mainloop()

    selected_path = app.selected_file_path
