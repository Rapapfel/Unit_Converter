import customtkinter as ctk

class unit_status_frame(ctk.CTkToplevel):
    def __init__(self, root, einheit):
        super().__init__(root)
        self.title("Einheitsinformation")
        self.geometry("400x200")
        self.attributes("-topmost",True)

        self.einheit = einheit
        self.root = root
        self.widgets_erstellen()
        self.fenster_zentrieren()

    def widgets_erstellen(self):
        # Nachricht über die Einheit des IFCs
        nachricht = f"Das ausgewählte IFC wurde mit {self.einheit} erstellt."
        self.Einheitsinformation = ctk.CTkLabel(self, text=nachricht)
        self.Einheitsinformation.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        # OK-Schaltfläche zum Schließen des Fensters
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.fenster_schliessen)
        self.ok_button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

    def fenster_zentrieren(self):
        root_x = self.master.winfo_x()
        root_y = self.master.winfo_y()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()

        x_position = root_x + (root_width - 400) // 2
        y_position = root_y + (root_height - 200) // 2

        self.geometry(f"+{x_position}+{y_position}")

    def fenster_schliessen(self):
        self.quit()
        self.destroy()
        

if __name__ == "__main__":
    # Erstellen und Anzeigen des Fensters mit der Nachricht über SI-Einheiten
    app = unit_status_frame("SI")
    app.mainloop()
