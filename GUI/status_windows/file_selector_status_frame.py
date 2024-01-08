import customtkinter as ctk

class file_selctor_status_frame(ctk.CTkToplevel):
    def __init__(self):
        """
        Konstruktor für die file_selctor_status_frame-Klasse.
        """
        super().__init__()
        self.title("Fehlermeldung")
        self.geometry("450x200")
        self.attributes("-topmost", True)

        self.widgets_erstellen()

    def widgets_erstellen(self):
        """
        Erstellt die GUI-Elemente im Toplevel-Fenster.
        """
        # Beschriftung für die Fehlermeldung
        self.fehlermeldung = ctk.CTkLabel(self, text="Die ausgewählte Datei konnte nicht geladen werden. Versuchen Sie es erneut!")
        self.fehlermeldung.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        # OK-Schaltfläche zum Schließen des Fensters
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.fenster_schliessen)
        self.ok_button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

    def fenster_schliessen(self):
        """
        Aktion, die beim Klicken auf die "OK"-Schaltfläche ausgeführt wird, um das Fenster zu schließen.
        """
        self.destroy()

# Hauptprogramm
if __name__ == "__main__":
    # Erstellen eines Hauptfensters
    root = ctk.CTk()
    root.geometry("800x600")  # Beispielgröße

    # Erstellen und Anzeigen des file_selector_status_frame Fensters
    status_frame = file_selctor_status_frame()
    status_frame.mainloop()
