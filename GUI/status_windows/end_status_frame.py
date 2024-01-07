import customtkinter as ctk

class end_status_frame(ctk.CTkFrame):
    def __init__(self, master, X, Y):
        self.fg_color = "#242424"
        super().__init__(master, width=X,height=Y, fg_color=self.fg_color)

        self.widgets_erstellen()

    def widgets_erstellen(self):
        # Beschriftung für die Feritginformation
        text1 = "Die Einheiten der gewählten IFC-Datei wurden umgewandelt und"
        text2 = "eine neue IFC-Datei unter ihrem angegebenen Pfad abgespeichert"

        label1 = ctk.CTkLabel(self, text=text1)
        label1.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

        label2 = ctk.CTkLabel(self, text=text2)
        label2.place(relx=0.5, rely=0.49, anchor=ctk.CENTER)

        # Beenden-Schaltfläche zum Schließen des Fensters und Programms
        self.end_button = ctk.CTkButton(self, text="Beenden", command=self.fenster_schliessen)
        self.end_button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

    def fenster_schliessen(self):
        self.quit()

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
    frame = end_status_frame(root, window_width - 60, window_height)
    frame.pack(fill="both", expand=True)

    # Starten des Event-Loops
    root.mainloop()
