import customtkinter as ctk

class EinheitenKonverter(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Einheitenkonverter")
        self.geometry("500x300")

        self.einheitenauswahl = ctk.StringVar(value="SI")  # Standardauswahl auf "SI" setzen
        self.widgets_erstellen()

    def widgets_erstellen(self):
        # Beschriftung
        self.beschriftung = ctk.CTkLabel(self, text="Bitte wählen Sie aus, in welche Einheiten das IFC konvertiert werden soll")
        self.beschriftung.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        # Abbrechen-Button
        self.abbrechen_button = ctk.CTkButton(self, text="Abbrechen", command=self.abbrechen_aktion)
        self.abbrechen_button.place(relx=0.3, rely=0.8, anchor=ctk.CENTER)

        # Weiter-Button
        self.weiter_button = ctk.CTkButton(self, text="Weiter", command=self.weiter_aktion)
        self.weiter_button.place(relx=0.7, rely=0.8, anchor=ctk.CENTER)

        # Radiobuttons für die Auswahl der Einheiten
        self.si_radiobutton = ctk.CTkRadioButton(self, text="SI-Einheiten", variable=self.einheitenauswahl, value="SI-Einheiten")
        self.si_radiobutton.place(relx=0.3, rely=0.3, )
        
        self.imperial_radiobutton = ctk.CTkRadioButton(self, text="Imperial-Einheiten", variable=self.einheitenauswahl, value="Imperial-Einheiten")
        self.imperial_radiobutton.place(relx=0.3, rely=0.4)

        self.hlks_radiobutton = ctk.CTkRadioButton(self, text="HVAC-Einheiten", variable=self.einheitenauswahl, value="HVAC-Einheiten")
        self.hlks_radiobutton.place(relx=0.3, rely=0.5)

        self.benutzerdefiniert_radiobutton = ctk.CTkRadioButton(self, text="Benutzerdefinierte Vorlage", variable=self.einheitenauswahl, value="Benutzerdefinierte Vorlage")
        self.benutzerdefiniert_radiobutton.place(relx=0.3, rely=0.6)

    def weiter_aktion(self):
        # Platzhalter für die Aktion, die ausgeführt werden soll, wenn 'Weiter' geklickt wird
        pass

    def abbrechen_aktion(self):
        self.destroy()

if __name__ == "__main__":
    app = EinheitenKonverter()
    app.mainloop()
