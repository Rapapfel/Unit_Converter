import customtkinter as ctk

class export_template_status_frame(ctk.CTkToplevel):
    def __init__(self,container, root):
        super().__init__()
        self.title("Exportinformation")
        self.geometry("450x200")
        self.attributes("-topmost",True)

        self.container = container
        self.root = root
        self.widgets_erstellen()
        self.fenster_zentrieren()


    def fenster_zentrieren(self):
        root_x = self.master.winfo_x()
        root_y = self.master.winfo_y()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()

        x_position = root_x + (root_width - 400) // 2
        y_position = root_y + (root_height - 200) // 2

        self.geometry(f"+{x_position}+{y_position}")

    def widgets_erstellen(self):
        # Beschriftung für die Exportinformation
        self.Exportinformation = ctk.CTkLabel(self, text="Die Vorlage wurde erfolgreich abgespeichert!")
        self.Exportinformation.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        # OK-Schaltfläche zum Schließen des Fensters
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.fenster_schliessen)
        self.ok_button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

    def fenster_schliessen(self):
        self.container.export_template_status_frame_callback()
        self.destroy()

if __name__ == "__main__":
    # Erstellen eines Hauptfensters
    root = ctk.CTk()
    root.geometry("800x600")  # Beispielgröße

    # Container könnte das Hauptfenster oder ein anderes Element sein, das die Callbacks definiert
    container = root  # In diesem Beispiel wird das Hauptfenster als Container verwendet

    # Erstellen Sie das export_template_status_frame Fenster
    status_frame = export_template_status_frame(container, root)
    status_frame.mainloop()
