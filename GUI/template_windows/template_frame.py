import json
import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class BenutzerdefinierteVorlagen(ctk.CTkFrame):
    def __init__(self, container, X, Y):
        """
        Konstruktor der BenutzerdefinierteVorlagen-Klasse.

        Parameter:
        - container: Tkinter-Container, in dem das Frame platziert wird.
        - X: Breite des Frames.
        - Y: Höhe des Frames.
        """
        self.fg_color = "#242424"
        super().__init__(container,width=X, height=Y, fg_color=self.fg_color)
        self.container = container
        self.font_size = ("Arial", 18)

        # Relativer Pfad zu den benutzerdefinierten Vorlagen
        self.templates_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'Templates', 'custom_templates')

        # Beschriftung
        self.beschriftung = ctk.CTkLabel(self, text="Wähle eine benutzerdefinierte Vorlage aus", fg_color=self.fg_color, text_color="white")
        self.beschriftung.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        # Knöpfe (kleiner gemacht und oben angezeigt)
        self.button_frame = ctk.CTkFrame(self,width=700,height=40, fg_color=self.fg_color)
        self.button_frame.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        self.neu_button = ctk.CTkButton(self.button_frame, text="Neu", width=80, height=24, command=self.neu_button_aktion)
        self.neu_button.pack(side="left", padx=5, pady=5)

        self.bearbeiten_button = ctk.CTkButton(self.button_frame, text="Bearbeiten", width=80, height=24, command=self.bearbeiten_button_aktion)
        self.bearbeiten_button.pack(side="left", padx=5)

        self.löschen_button = ctk.CTkButton(self.button_frame, text="Löschen", width=80, height=24, command=self.löschen_button_aktion)
        self.löschen_button.pack(side="left", padx=5)

        self.import_button = ctk.CTkButton(self.button_frame, text="Import", width=80, height=24, command=self.import_button_aktion)
        self.import_button.pack(side="left", padx=5)

        self.export_button = ctk.CTkButton(self.button_frame, text="Export", width=80, height=24, command=self.export_button_aktion)
        self.export_button.pack(side="left", padx=5)

        # Rahmen um die Tabelle
        self.table_frame = ctk.CTkFrame(self, fg_color=self.fg_color)
        self.table_frame.pack(fill="both", expand=False, padx=10)

        # Erstellen Sie eine Treeview mit maximal 7 Zeilen sichtbar
        style = ttk.Style()
        self.table = ttk.Treeview(self.table_frame, columns=("Name", "Datum", "Von", "Beschreibung"), show="headings", height=10)
        style.configure("Treeview", rowheight=35)
        self.table.heading("Name", text="Vorlagenname", anchor="w")
        self.table.heading("Datum", text="Zuletzt geändert", anchor="w")
        self.table.heading("Von", text="Geändert von", anchor="w")
        self.table.heading("Beschreibung", text="Beschreibung", anchor="w")
        self.table.pack(side="left", fill="both", expand=True)

        # Stil für den Treeview
        style = ttk.Style()
        style.configure("Treeview", background=self.fg_color, fieldbackground=self.fg_color, foreground=self.fg_color, font=self.font_size)
        style.map("Treeview", background=[("selected", "#0078d7")], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", font=self.font_size)
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # Farben für die Tabelle und Überschriften setzen
        self.table.tag_configure("evenrow", background="#242424", foreground="white", font=self.font_size)
        self.table.tag_configure("oddrow", background="#323232", foreground="white", font=self.font_size)

        # Scrollbar für die Tabelle rechts neben der Tabelle platzieren
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=self.scrollbar.set)

        # Große Knöpfe
        self.abbruch_button = ctk.CTkButton(self, text="Abbrechen", command=self.abbrechen_aktion, width=120, height=32)
        self.abbruch_button.place(relx=0.4, rely=0.7, anchor=ctk.CENTER)

        self.weiter_button = ctk.CTkButton(self, text="Weiter", width=120, height=32, command=self.weiter_button_aktion)
        self.weiter_button.place(relx=0.6, rely=0.7, anchor=ctk.CENTER)

        # Vorlagen laden
        self.load_templates()

        # Spaltenbreite anpassen
        self.set_initial_column_width()

        # Tabelle horizontal in der Mitte des Fensters zentrieren
        self.table_frame.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

    def load_templates(self):
        """
        Lädt die Vorlagendaten aus den Dateien und fügt sie der Tabelle hinzu.
        """
        for index, filename in enumerate(os.listdir(self.templates_dir)):
            if filename.endswith(".json"):
                file_path = os.path.join(self.templates_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    row_tag = "evenrow" if index % 2 == 0 else "oddrow"
                    self.table.insert("", "end", values=(data["template_name"], data["last_modified"], data["modified_by"], data["description"]), tags=(row_tag,))

    def set_initial_column_width(self):
        """
        Setzt die anfängliche Breite der Spalten in der Tabelle.
        """
        self.table.column("Name", width=350, stretch=tk.NO)
        self.table.column("Datum", width=300, stretch=tk.NO)
        self.table.column("Von", width=200, stretch=tk.NO)
        self.table.column("Beschreibung", width=900, stretch=tk.NO)
    
    def neu_button_aktion(self):
        """
        Aktion, die ausgeführt wird, wenn der "Neu" Button geklickt wird.
        """
        if self.neu_button:
            self.container.neu_template_frame_callback()
    
    def löschen_button_aktion(self):
        """
        Aktion, die ausgeführt wird, wenn der "Löschen" Button geklickt wird.
        """
        selected_item = self.table.focus()
        if selected_item:
            item_data = self.table.item(selected_item, "values")
            if item_data:
                template_name = item_data[0]
                self.container.löschen_template_frame_callback(template_name)
    
    def import_button_aktion(self):
        """
        Aktion, die ausgeführt wird, wenn der "Import" Button geklickt wird.
        """
        self.container.import_template_frame_callback()

    def export_button_aktion(self):
        """
        Aktion, die ausgeführt wird, wenn der "Export" Button geklickt wird.
        """
        selected_item = self.table.focus()
        if selected_item:
            item_data = self.table.item(selected_item, "values")
            if item_data:
                template_name = item_data[0]
                self.container.export_template_frame_callback(template_name)
        
    def bearbeiten_button_aktion(self):
        """
        Bearbeitet die ausgewählte Vorlage, indem sie die Vorlagendaten lädt und an die entsprechende Methode im Container weitergibt.
        """
        # Das ausgewählte Element in der Tabelle erhalten
        selected_item = self.table.focus()
        if selected_item:
            # Daten des ausgewählten Elements abrufen
            item_data = self.table.item(selected_item, "values")
            if item_data:
                # Name der Vorlage aus den Daten extrahieren
                template_name = item_data[0]
                self.container.set_current_template_name(template_name)  # Neu hinzugefügt
                # Pfad zur Vorlagendatei erstellen
                file_path = os.path.join(self.templates_dir, f"{template_name}.json")
                # Vorlagendaten aus der Datei laden
                with open(file_path, 'r', encoding='utf-8') as file:
                    template_data = json.load(file)
                # Callback-Funktion im Container aufrufen und Vorlagendaten übergeben
                self.container.bearbeiten_template_frame_callback(template_data)


    def weiter_button_aktion(self):
        """
        Fährt mit der Bearbeitung der ausgewählten Vorlage fort, indem die Vorlage verarbeitet und das Ergebnis gespeichert wird.
        """
        # Die ID des ausgewählten Elements in der Tabelle erhalten
        selected_item = self.table.focus()
        if selected_item:
            # Daten des ausgewählten Elements abrufen
            item_data = self.table.item(selected_item, "values")
            if item_data and len(item_data) > 0:
                # Name der ausgewählten Vorlage extrahieren
                template_name = item_data[0]
                # Methode im Container aufrufen, um die ausgewählte Vorlage zu verarbeiten
                self.container.process_selected_template(template_name)
                # Callback-Funktion im Container aufrufen, um das Ergebnis zu speichern
                self.container.file_saver_frame_callback()
                

    def abbrechen_aktion(self):
        """
        Beendet die Anwendung.
        """
        # Die Methode im Container aufrufen, um die Anwendung zu beenden
        self.container.abbrechen()

if __name__ == "__main__":
    # Erstellen eines Hauptfensters
    root = ctk.CTk()

    # Konfiguration der Fenstergröße und Position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = (3 * screen_width) // 4
    window_height = (2 * screen_height) // 3
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Instanziieren und Anzeigen des BenutzerdefinierteVorlagen Frames
    benutzerdefinierte_vorlagen_frame = BenutzerdefinierteVorlagen(root, window_width, window_height)
    benutzerdefinierte_vorlagen_frame.pack(fill="both", expand=True)

    # Starten des Event-Loops
    root.mainloop()
