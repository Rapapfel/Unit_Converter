import customtkinter as ctk

class export_template_status_frame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Exportinformation")
        self.geometry("450x200")
        self.attributes("-topmost",True)

        self.widgets_erstellen()

    def widgets_erstellen(self):
        # Beschriftung für die Exportinformation
        self.Exportinformation = ctk.CTkLabel(self, text="Die Vorlage wurde erfolgreich abgespeichert!")
        self.Exportinformation.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        # OK-Schaltfläche zum Schließen des Fensters
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.fenster_schliessen)
        self.ok_button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

    def fenster_schliessen(self):
        self.destroy()

if __name__ == "__main__":
    app = export_template_status_frame()
    app.mainloop()
