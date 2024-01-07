import customtkinter as ctk

class Unit_selector(ctk.CTkFrame):
    def __init__(self, container, X, Y):
        self.fg_color = "#242424"
        super().__init__(container,width=X,height=Y, fg_color=self.fg_color)
        self.container = container

        self.einheitenauswahl = ctk.StringVar(value="SI")  # Standardauswahl auf "SI" setzen
        self.widgets_erstellen()

    def widgets_erstellen(self):
        # Beschriftung
        self.beschriftung = ctk.CTkLabel(self, text="Bitte wählen Sie aus, in welche Einheiten das IFC konvertiert werden soll")
        self.beschriftung.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)

        # Abbrechen-Button
        self.abbrechen_button = ctk.CTkButton(self, text="Abbrechen", command=self.abbrechen_aktion)
        self.abbrechen_button.place(relx=0.4, rely=0.7, anchor=ctk.CENTER)

        # Weiter-Button
        self.weiter_button = ctk.CTkButton(self, text="Weiter", command=self.weiter_aktion)
        self.weiter_button.place(relx=0.6, rely=0.7, anchor=ctk.CENTER)

        # Radiobuttons für die Auswahl der Einheiten
        self.si_radiobutton = ctk.CTkRadioButton(self, text="SI-Einheiten", variable=self.einheitenauswahl, value="SI-Einheiten")
        self.si_radiobutton.place(relx=0.425, rely=0.425)
        
        self.imperial_radiobutton = ctk.CTkRadioButton(self, text="Imperial-Einheiten", variable=self.einheitenauswahl, value="Imperial-Einheiten")
        self.imperial_radiobutton.place(relx=0.425, rely=0.475)

        self.hlks_radiobutton = ctk.CTkRadioButton(self, text="HVAC-Einheiten", variable=self.einheitenauswahl, value="HVAC-Einheiten")
        self.hlks_radiobutton.place(relx=0.425, rely=0.525)

        self.benutzerdefiniert_radiobutton = ctk.CTkRadioButton(self, text="Benutzerdefinierte Vorlage", variable=self.einheitenauswahl, value="Benutzerdefinierte Vorlage")
        self.benutzerdefiniert_radiobutton.place(relx=0.425, rely=0.575)

    def weiter_aktion(self):
        if self.benutzerdefiniert_radiobutton:
            self.container.unit_selector_callback()

    def abbrechen_aktion(self):
        # Die Anwendung schließen
        self.container.abbrechen()

if __name__ == "__main__":
    # Erstellen des Hauptfensters
    root = ctk.CTk()

    # Konfiguration der Fenstergröße und Position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = (3 * screen_width) // 4
    window_height = (2 * screen_height) // 3
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Instanziieren und Anzeigen des Frames
    frame = Unit_selector(root, window_width - 60, window_height)
    frame.pack(fill="both", expand=True)

    # Starten des Event-Loops
    root.mainloop()

