import customtkinter as ctk

class DeleteTemplateConfirmation(ctk.CTkToplevel):
    """
    Klasse zur Erstellung eines Bestätigungsfensters für das Löschen einer Vorlage.

    Attribute:
    - template_name: Name der zu löschenden Vorlage.
    - container: Übergeordnetes Tkinter-Container-Objekt, das die Callbacks definiert.
    """
    def __init__(self, root, template_name, container):
        """
        Konstruktor der DeleteTemplateConfirmation-Klasse.

        Parameter:
        - root: Tkinter-Root-Fenster.
        - template_name: Name der zu löschenden Vorlage.
        - container: Tkinter-Container, der die Callbacks definiert.
        """
        super().__init__()
        self.title("Vorlage löschen")
        self.geometry("450x150")
        self.attributes("-topmost", True)
        self.container = container

        self.template_name = template_name
        self.root = root
        self.widgets_erstellen()
        self.fenster_zentrieren()

    def fenster_zentrieren(self):
        """
        Zentriert das Bestätigungsfenster über dem Hauptfenster.
        """
        root_x = self.master.winfo_x()
        root_y = self.master.winfo_y()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()

        x_position = root_x + (root_width - 400) // 2
        y_position = root_y + (root_height - 200) // 2

        self.geometry(f"+{x_position}+{y_position}")
    
    def widgets_erstellen(self):
        """
        Erstellt und platziert die Widgets im Fenster.
        """
        # Meldungstext mit dem übergebenen Vorlagennamen
        message_text = f"Soll die Vorlage '{self.template_name}' gelöscht werden?"
        message_label = ctk.CTkLabel(self, text=message_text)
        message_label.pack(pady=20)

        # Funktionen zum Handhaben der Schaltflächen
        def yes_action():
            # Callback-Methode für die Zustimmung zur Löschung
            self.container.yes_löschen_template_callback(self.template_name)
            self.destroy()

        def no_action():
            # Schließen des Fensters ohne Aktion
            self.destroy()

        # Buttons für "Ja" und "Nein"
        yes_button = ctk.CTkButton(self, text="Ja", command=yes_action)
        yes_button.place(relx=0.7, rely=0.8, anchor=ctk.CENTER)

        no_button = ctk.CTkButton(self, text="Nein", command=no_action)
        no_button.place(relx=0.3, rely=0.8, anchor=ctk.CENTER)

# Hauptfenster-Erstellung und -Konfiguration
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")  # Beispielgröße

    # Beispiel für den Namen der zu löschenden Vorlage
    template_name = "Name der Vorlage"

    # Container könnte das Hauptfenster oder ein anderes Element sein, das die Callbacks definiert
    container = root

    # Erstellung des Bestätigungsfensters
    delete_confirmation_window = DeleteTemplateConfirmation(root, template_name, container)
    delete_confirmation_window.mainloop()
