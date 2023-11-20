import tkinter as tk
import customtkinter as ctk

class DeleteTemplateConfirmation(ctk.CTk):
    def __init__(self, template_name):
        super().__init__()
        self.title("Vorlage löschen")
        self.geometry("450x150")

        # Meldungstext mit dem übergebenen Vorlagennamen
        message_text = f"Soll die Vorlage '{template_name}' gelöscht werden?"
        message_label = ctk.CTkLabel(self, text=message_text)
        message_label.pack(pady=20)

        # Funktion zum Handhaben der "Ja"-Schaltfläche
        def yes_action():
            # Fügen Sie hier Ihren Code zur tatsächlichen Löschung der Vorlage ein
            # Zum Beispiel: Löschung der Datei oder des Eintrags in einer Datenbank
            # Hier wird nur eine Meldung angezeigt und das Hauptfenster geschlossen
            print(f"Vorlage '{template_name}' wurde gelöscht.")
            self.destroy()

        # Funktion zum Handhaben der "Nein"-Schaltfläche
        def no_action():
            # Fügen Sie hier Ihren Code für den Fall hinzu, dass "Nein" ausgewählt wurde
            print(f"Löschung der Vorlage '{template_name}' abgebrochen.")
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
