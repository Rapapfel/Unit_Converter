import customtkinter as ctk

class DeleteTemplateConfirmation(ctk.CTkToplevel):
    def __init__(self, root, template_name,container):
        super().__init__()
        self.title("Vorlage löschen")
        self.geometry("450x150")
        self.attributes("-topmost",True)
        self.container = container

        self.template_name = template_name
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
        # Meldungstext mit dem übergebenen Vorlagennamen
        message_text = f"Soll die Vorlage '{self.template_name}' gelöscht werden?"
        message_label = ctk.CTkLabel(self, text=message_text)
        message_label.pack(pady=20)

        # Funktion zum Handhaben der "Ja"-Schaltfläche
        def yes_action():
            # Fügen Sie hier Ihren Code zur tatsächlichen Löschung der Vorlage ein
            # Zum Beispiel: Löschung der Datei oder des Eintrags in einer Datenbank
            # Hier wird nur eine Meldung angezeigt und das Hauptfenster geschlossen
            print(f"Vorlage '{self.template_name}' wurde gelöscht.")
            self.container.yes_löschen_template_callback(self.template_name)
            self.destroy()

        # Funktion zum Handhaben der "Nein"-Schaltfläche
        def no_action():
            # Fügen Sie hier Ihren Code für den Fall hinzu, dass "Nein" ausgewählt wurde
            print(f"Löschung der Vorlage '{self.template_name}' abgebrochen.")
            self.destroy()

        # Button für "Ja"
        yes_button = ctk.CTkButton(self, text="Ja", command=yes_action)
        yes_button.place(relx=0.7, rely=0.8, anchor=ctk.CENTER)

        # Button für "Nein"
        no_button = ctk.CTkButton(self, text="Nein", command=no_action)
        no_button.place(relx=0.3, rely=0.8, anchor=ctk.CENTER)

if __name__ == "__main__":
    # Nehmen Sie an, dass Sie den Namen der Vorlage haben, z.B., "Name der Vorlage"
    template_name = "Name der Vorlage"
    
    # Erstellen Sie das DeleteTemplateConfirmation-Fenster und übergeben Sie den Vorlagennamen
    delete_confirmation_window = DeleteTemplateConfirmation(template_name)
    delete_confirmation_window.mainloop()
