import customtkinter as ctk

class unit_status_frame(ctk.CTkToplevel):
    def __init__(self, einheit):
        super().__init__()
        self.title("Einheitsinformation")
        self.geometry("400x200")

        self.einheit = einheit
        self.widgets_erstellen()

    def widgets_erstellen(self):
        # Nachricht über die Einheit des IFCs
        nachricht = f"Das ausgewählte IFC wurde mit {self.einheit}-Einheiten erstellt."
        self.Einheitsinformation = ctk.CTkLabel(self, text=nachricht)
        self.Einheitsinformation.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        # OK-Schaltfläche zum Schließen des Fensters
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.fenster_schliessen)
        self.ok_button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

    def fenster_schliessen(self):
        self.destroy()
        

if __name__ == "__main__":
    # Erstellen und Anzeigen des Fensters mit der Nachricht über SI-Einheiten
    app = unit_status_frame("SI")
    app.mainloop()
