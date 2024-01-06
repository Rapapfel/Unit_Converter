import customtkinter as ctk
from tkinter import filedialog

class IFC_File_Saver_frame(ctk.CTkFrame):
    def __init__(self, container, X, Y):
        self.fg_color = "#242424"
        super().__init__(container,width=X,height=Y, fg_color=self.fg_color)
        self.container = container

        self.widgets_erstellen()

    def widgets_erstellen(self):
        # Beschriftung
        self.beschriftung = ctk.CTkLabel(self, text="Bitte wählen Sie den Dateipfad, um die neue IFC-Datei zu speichern")
        self.beschriftung.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
        
        # Schaltfläche, um abzubrechen und die Anwendung zu schließen (Links)
        self.abbrechen_schaltflaeche = ctk.CTkButton(self, text="Abbrechen", command=self.anwendung_schliessen)
        self.abbrechen_schaltflaeche.place(relx=0.3, rely=0.6, anchor=ctk.CENTER)
        
        # Schaltfläche, um den Dateipfad auszuwählen (Mitte)
        self.waehlen_schaltflaeche = ctk.CTkButton(self, text="Wählen", command=self.dateipfad_auswaehlen)
        self.waehlen_schaltflaeche.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        
        # Schaltfläche, um die Datei zu speichern (Rechts)
        self.speichern_schaltflaeche = ctk.CTkButton(self, text="Speichern", command=self.datei_speichern)
        self.speichern_schaltflaeche.place(relx=0.7, rely=0.6, anchor=ctk.CENTER)

        # Eingabefeld für den Dateipfad
        self.dateipfad_eingabe = ctk.CTkEntry(self, width=600, state='disabled', placeholder_text="VAR_DATEIPFAD")
        self.dateipfad_eingabe.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

    def dateipfad_auswaehlen(self):
        # Einen Datei-Dialog öffnen, um einen Speicherort auszuwählen und den Pfad im Eingabefeld anzeigen
        dateipfad = filedialog.asksaveasfilename(defaultextension=".ifc")
        if dateipfad:
            self.selected_save_file_path = dateipfad  # Speichern des Pfades als Attribut der Klasse
            self.dateipfad_eingabe.configure(state='normal')  # Aktiviert das Eingabefeld, um den Text zu ändern
            self.dateipfad_eingabe.delete(0, ctk.END)
            self.dateipfad_eingabe.insert(0, dateipfad)
            self.dateipfad_eingabe.configure(state='disabled')  # Deaktiviert das Eingabefeld wieder

    def datei_speichern(self):
        if self.selected_save_file_path:
            self.container.process_selected_save_file_path(self.selected_save_file_path)
            self.container.extract_data_and_update_ifc_callback()
            self.container.end_status_frame_callback()

    def anwendung_schliessen(self):
        # Die Anwendung schließen
        self.destroy()