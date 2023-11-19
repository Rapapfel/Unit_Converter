import json
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os

# Die Hauptklasse für die GUI-Anwendung erstellen
class HLKSEinstellungen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HLKS-Einheiten Einstellungen")
        self.geometry("350x600")

        # Das Verzeichnis für Vorlagen festlegen
        self.templates_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')

        # Farben definieren
        self.bg_color = "#242424"
        self.text_color = "#ffffff"
        self.selected_tab_color = "#0078d7"

        # Stil für die GUI-Elemente konfigurieren
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background=self.bg_color, foreground=self.text_color, padding=[10, 3.5])
        style.configure('TFrame', background=self.bg_color)
        style.map('TNotebook.Tab', background=[('selected', self.selected_tab_color)], foreground=[('selected', self.text_color)])

        # Registerkarten erstellen
        self.tab_control = ttk.Notebook(self, style='TNotebook')

        # Registerkarten für Heizung, Lüftung und Sanitär erstellen
        self.tab_heizung = self.create_scrollable_tab("Heizung")
        self.tab_lueftung = self.create_scrollable_tab("Lüftung")
        self.tab_sanitaer = self.create_scrollable_tab("Sanitär")

        self.tab_control.pack(expand=1, fill="both")

        # Rahmen für Schaltflächen erstellen
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side="bottom", pady=10)

        # "Abbrechen"-Schaltfläche erstellen
        self.abbruch_button = ctk.CTkButton(self.button_frame, text="Abbrechen", command=self.quit)
        self.abbruch_button.pack(side="left", padx=10)  # Button "Abbrechen" links

        # "Weiter"-Schaltfläche erstellen
        self.weiter_button = ctk.CTkButton(self.button_frame, text="Weiter", command=self.weiter_aktion)
        self.weiter_button.pack(side="right", padx=10)  # Button "Weiter" rechts

        # Einstellungen laden
        self.load_einstellungen()

    # Methode zum Erstellen einer scrollbaren Registerkarte
    def create_scrollable_tab(self, title):
        tab = ttk.Frame(self.tab_control, style='TFrame')
        self.tab_control.add(tab, text=title)

        scrollbar = tk.Scrollbar(tab, orient="vertical", troughcolor=self.bg_color, bg=self.bg_color)
        scrollbar.pack(side="right", fill="y")

        canvas = tk.Canvas(tab, yscrollcommand=scrollbar.set, bg=self.bg_color, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)

        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Überschriften für Parameter und Zieleinheit hinzufügen
        parameter_label = ctk.CTkLabel(scrollable_frame, text="Parameter", anchor="w", fg_color=self.bg_color, text_color=self.text_color, font=("Helvetica", 12, "bold"))
        parameter_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        zieleinheit_label = ctk.CTkLabel(scrollable_frame, text="Zieleinheit", anchor="w", fg_color=self.bg_color, text_color=self.text_color, font=("Helvetica", 12, "bold"))
        zieleinheit_label.grid(row=0, column=1, padx=10, pady=5)

        separator = ttk.Separator(scrollable_frame, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        # Anpassen des Scrollbereichs, wenn sich die Größe ändert
        scrollable_frame.bind("<Configure>", lambda e, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        # Scrollen mit dem Mausrad ermöglichen
        canvas.bind_all("<MouseWheel>", lambda event, canvas=canvas: self.scroll_canvas_area(event, canvas))

        canvas.bind("<Enter>", lambda event, canvas=canvas: canvas.bind_all("<MouseWheel>", lambda event, canvas=canvas: self.scroll_canvas_area(event, canvas)))
        canvas.bind("<Leave>", lambda event, canvas=canvas: canvas.unbind_all("<MouseWheel>"))

        return scrollable_frame

    # Methode zum Laden der Einstellungen aus JSON-Dateien
    def load_einstellungen(self):
        self.einstellungen_anzeigen(self.tab_heizung, os.path.join(self.templates_dir, "HVAC_units_HEI.json"))
        self.einstellungen_anzeigen(self.tab_lueftung, os.path.join(self.templates_dir, "HVAC_units_LUF.json"))
        self.einstellungen_anzeigen(self.tab_sanitaer, os.path.join(self.templates_dir, "HVAC_units_SAN.json"))

    # Methode zum Anzeigen der Einstellungen auf einer Registerkarte
    def einstellungen_anzeigen(self, scrollable_frame, json_file):
        try:
            with open(json_file, "r") as file:
                einstellungen = json.load(file)
                for index, (parameter, einheit) in enumerate(einstellungen.items()):
                    label = ctk.CTkLabel(scrollable_frame, text=parameter, anchor="w", fg_color=self.bg_color, text_color=self.text_color)
                    label.grid(row=index + 2, column=0, sticky="w", padx=10, pady=5)
                    entry = ctk.CTkEntry(scrollable_frame, textvariable=tk.StringVar(value=einheit), fg_color=self.bg_color, text_color=self.text_color)
                    entry.grid(row=index + 2, column=1, padx=10, pady=5)
        except FileNotFoundError:
            print(f"Fehler: Datei {json_file} nicht gefunden.")

    # Methode für die Aktion, die beim Klicken auf die "Weiter"-Schaltfläche ausgeführt wird
    def weiter_aktion(self):
        pass

    # Methode zum Scrollen im Canvas-Bereich mit dem Mausrad
    def scroll_canvas_area(self, event, canvas):
        if event.delta:
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Hauptprogramm
if __name__ == "__main__":
    app = HLKSEinstellungen()
    app.mainloop()
