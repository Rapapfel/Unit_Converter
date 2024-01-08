import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
import json

class Neu_template_frame(ctk.CTkFrame):
    """
    Eine Klasse zur Erstellung eines Benutzeroberflächen-Elements für die Eingabe und Bearbeitung von Template-Daten.

    Attribute:
    container (CTk): Der übergeordnete Container für dieses Frame.
    X (int): Die Breite des Frames.
    Y (int): Die Höhe des Frames.
    parameter_dict (dict): Ein Wörterbuch, das die Parameter für das Template enthält.
    name_template (str): Der Name des Templates.
    bearbeitet_durch (str): Die Person, die das Template bearbeitet hat.
    beschreibung_template (str): Eine Beschreibung des Templates.
    """

    def __init__(self, container, X, Y, parameter_dict, name_template="", bearbeitet_durch="", beschreibung_template=""):
        """Initialisiert das Neu_template_frame mit den gegebenen Parametern."""
        self.fg_color = "#242424"
        super().__init__(container, width=X, height=Y, fg_color=self.fg_color)
        # Initialisierung der Attribute und Einstellungen
        self.container = container
        self.parameter_dict = parameter_dict
        self.name_template = name_template
        self.bearbeitet_durch = bearbeitet_durch
        self.beschreibung_template = beschreibung_template
        self.font_size = ("Arial", 18)
        self.option_add('*TCombobox*Font', ('Arial', 15))

        # Laden und Konfigurieren der Einheiten aus einer JSON-Datei
        current_script = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_script, "..", "..", "IFC_operation\\units\\units.json")
        with open(json_path, "r") as file:
            self.unit_categories = json.load(file)

        style = ttk.Style()
        style.theme_use('clam')
        # Stil-Einstellungen für das Aussehen der Comboboxen
        style.configure("TCombobox", fieldbackground=self.fg_color, background=self.fg_color, foreground="white", arrowcolor="white")
        style.map("TCombobox", fieldbackground=[("readonly", self.fg_color)], selectbackground=[("readonly", self.fg_color)], selectforeground=[("readonly", "white")])

        # Container für das Scrollable-Frame
        self.container_frame = ctk.CTkFrame(self, fg_color=self.fg_color)
        self.container_frame.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.4, anchor=ctk.W)

        # Canvas und Scrollbar für dynamische Inhalte
        self.canvas = tk.Canvas(self.container_frame, bg=self.fg_color, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.container_frame, command=self.canvas.yview, fg_color=self.fg_color)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame für das Hinzufügen von Inhalten
        self.grid_frame = ctk.CTkFrame(self.canvas, fg_color=self.fg_color)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        self.rows = []

        # Hinzufügen der Spaltentitel und Initialisierung der Zeilen
        self.add_column_titles()
        self.add_row()

        # Buttons zur Steuerung des Templates
        self.add_row_button = ctk.CTkButton(self, text="+", command=self.add_row)
        self.add_row_button.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.abbrechen_aktion)
        self.cancel_button.place(relx=0.25, rely=0.85, anchor=ctk.CENTER)

        self.erstellen_button = ctk.CTkButton(self, text="Template erstellen", command=self.erstellen_aktion)
        self.erstellen_button.place(relx=0.75, rely=0.85, anchor=ctk.CENTER)

        # Eingabefelder für zusätzliche Template-Informationen
        self.name_template_entry = tk.Entry(self, background=self.fg_color, foreground="white", font=self.font_size)
        self.name_template_entry.place(relx=0.3, rely=0.1, relwidth=0.6)
        self.bearbeitet_durch_entry = tk.Entry(self, background=self.fg_color, foreground="white", font=self.font_size)
        self.bearbeitet_durch_entry.place(relx=0.3, rely=0.15, relwidth=0.6)
        self.beschreibung_template_entry = tk.Entry(self, background=self.fg_color, foreground="white", font=self.font_size)
        self.beschreibung_template_entry.place(relx=0.3, rely=0.2, relwidth=0.6)

        # Weitere Methoden zum Hinzufügen von Informationen
        self.add_info_entries()
    def add_column_titles(self):
        """
        Fügt Spaltentitel zur Benutzeroberfläche hinzu.

        Titel und Spaltenbreiten werden aus der 'titles' und 'column_widths' Liste genommen.
        """
        titles = ["Pset", "Parameter", "Einheitenkategorie", "Quelleinheit", "Zieleinheit", ""]
        column_widths = [100, 220, 150, 200, 200, 20]  # Definiert Spaltenbreiten
        row_height = 30  # Beispielhöhe, kann angepasst werden

        for i, (title, width) in enumerate(zip(titles, column_widths)):
            label = ctk.CTkLabel(self.grid_frame, text=title, fg_color=self.fg_color, width=width, height=row_height)
            label.grid(row=0, column=i, sticky="nsew")

            if title == "Parameter":
                self.grid_frame.grid_columnconfigure(i, minsize=220)

    def add_info_entries(self):
        """
        Fügt Informationen zur Benutzeroberfläche hinzu.

        Die Informationen werden aus der 'info_labels' Liste genommen.
        """
        info_labels = ["Name des Templates:", "Zuletzt bearbeitet durch:", "Beschreibung:"]
        for i, label_text in enumerate(info_labels):
            label = ctk.CTkLabel(self, text=label_text, fg_color=self.fg_color)
            label.place(relx=0.1, rely=0.1 + i * 0.05, anchor=ctk.W)

    def add_row(self):
        """
        Fügt eine neue Zeile zur Benutzeroberfläche hinzu.

        Eine neue Zeile wird nur hinzugefügt, wenn entweder keine Zeilen vorhanden sind oder alle vorhandenen Zeilen vollständig sind.
        """
        if not self.rows or all(self.is_row_complete(row) for row in self.rows):
            row_index = len(self.rows) + 1
            widgets = self.create_row_widgets(row_index)
            self.rows.append(widgets)
            self.update_scrollregion()

    def create_row_widgets(self, row_index):
        """
        Erstellt Widgets für eine neue Zeile in der Benutzeroberfläche.

        Diese Methode erstellt Dropdown-Menüs und Schaltflächen für eine neue Zeile basierend auf dem übergebenen Zeilenindex.

        Args:
            row_index (int): Der Index der neuen Zeile.

        Returns:
            list: Eine Liste von erstellten Widgets.
        """
        widgets = []

        # Dropdown-Menü für Pset
        pset_var = tk.StringVar()
        pset_dropdown = ttk.Combobox(self.grid_frame, textvariable=pset_var, values=list(self.parameter_dict.keys()), state="readonly", style="TCombobox", font=self.font_size)
        pset_dropdown.grid(row=row_index, column=0, sticky="nsew")
        widgets.append(pset_dropdown)

        # Dropdown-Menü für Parameter
        param_var = tk.StringVar()
        param_dropdown = ttk.Combobox(self.grid_frame, textvariable=param_var, state="readonly", style="TCombobox", font=self.font_size)
        param_dropdown.grid(row=row_index, column=1, sticky="nsew")
        widgets.append(param_dropdown)

        # Dropdown-Menü für Einheitenkategorie
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(self.grid_frame, textvariable=category_var, values=list(self.unit_categories.keys()), state="readonly", style="TCombobox", font=self.font_size)
        category_dropdown.grid(row=row_index, column=2, sticky="nsew")
        widgets.append(category_dropdown)

        # Dropdown-Menü für Quelleinheit
        source_unit_var = tk.StringVar()
        source_unit_dropdown = ttk.Combobox(self.grid_frame, textvariable=source_unit_var, state="readonly", style="TCombobox", font=self.font_size)
        source_unit_dropdown.grid(row=row_index, column=3, sticky="nsew")
        widgets.append(source_unit_dropdown)

        # Dropdown-Menü für Zieleinheit
        target_unit_var = tk.StringVar()
        target_unit_dropdown = ttk.Combobox(self.grid_frame, textvariable=target_unit_var, state="readonly", style="TCombobox")
        target_unit_dropdown.grid(row=row_index, column=4, sticky="nsew")
        widgets.append(target_unit_dropdown)

        # Schaltfläche zum Entfernen der Zeile
        remove_button = ctk.CTkButton(self.grid_frame, text="-", width=2, height=1, command=lambda: self.remove_row(row_index))
        remove_button.grid(row=row_index, column=5, sticky="nsew")
        widgets.append(remove_button)

        # Ereignisbindungen für Dropdown-Menüs
        pset_dropdown.bind("<<ComboboxSelected>>", lambda event, pset_dropdown=pset_dropdown, param_dropdown=param_dropdown: self.update_pset_dropdown(pset_dropdown, param_dropdown, source_unit_dropdown, target_unit_dropdown, category_dropdown))
        param_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_param_dropdown(source_unit_dropdown, target_unit_dropdown, category_dropdown))
        category_dropdown.bind("<<ComboboxSelected>>", lambda event, source_unit_dropdown=source_unit_dropdown, target_unit_dropdown=target_unit_dropdown: self.update_unit_dropdowns(category_dropdown, source_unit_dropdown, target_unit_dropdown))

        return widgets

    def update_scrollregion(self):
        """
        Aktualisiert die Scrollregion des Canvas basierend auf dem Inhalt der grid_frame.
        """
        self.grid_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def scroll_canvas_area(self, event, canvas):
        """
        Scrollt den Canvas-Bereich basierend auf dem Mausradereignis.

        Args:
            event (Event): Das Mausradereignis.
            canvas (Canvas): Der Canvas, der gescrollt werden soll.
        """
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def is_row_complete(self, row_widgets):
        """
        Überprüft, ob eine Zeile vollständig ausgefüllt ist.

        Args:
            row_widgets (list): Eine Liste von Widgets in der Zeile.

        Returns:
            bool: True, wenn alle Dropdown-Menüs in der Zeile ausgewählt sind, sonst False.
        """
        pset_dropdown, param_dropdown, category_dropdown, source_unit_dropdown, target_unit_dropdown, remove_button = row_widgets
        return pset_dropdown.get() and param_dropdown.get() and category_dropdown.get() and source_unit_dropdown.get() and target_unit_dropdown.get()

    def remove_row(self, row_index):
        """
        Entfernt eine Zeile aus der Benutzeroberfläche und aktualisiert die Scrollregion.

        Args:
            row_index (int): Der Index der zu entfernenden Zeile.
        """
        widgets_to_remove = self.rows.pop(row_index - 1)
        for widget in widgets_to_remove:
            widget.destroy()
        self.update_scrollregion()

    def update_pset_dropdown(self, pset_dropdown, param_dropdown, source_unit_dropdown, target_unit_dropdown, category_dropdown):
        """
        Aktualisiert das Parameter-Dropdown basierend auf der Auswahl im Pset-Dropdown.

        Args:
            pset_dropdown (ttk.Combobox): Das Pset-Dropdown-Menü.
            param_dropdown (ttk.Combobox): Das Parameter-Dropdown-Menü.
            source_unit_dropdown (ttk.Combobox): Das Dropdown-Menü für Quelleinheit.
            target_unit_dropdown (ttk.Combobox): Das Dropdown-Menü für Zieleinheit.
            category_dropdown (ttk.Combobox): Das Dropdown-Menü für Einheitenkategorie.
        """
        selected_pset = pset_dropdown.get()
        param_dropdown["values"] = self.parameter_dict[selected_pset]
        param_dropdown.set("")
        category_dropdown.set("")
        source_unit_dropdown.set("")
        target_unit_dropdown.set("")

    
    def update_param_dropdown(self, source_unit_dropdown, target_unit_dropdown, category_dropdown):
        """
        Aktualisiert die Dropdown-Menüs für Einheitenkategorie, Quelleinheit und Zieleinheit basierend auf der Auswahl im Parameter-Dropdown.

        Args:
            source_unit_dropdown (ttk.Combobox): Das Dropdown-Menü für Quelleinheit.
            target_unit_dropdown (ttk.Combobox): Das Dropdown-Menü für Zieleinheit.
            category_dropdown (ttk.Combobox): Das Dropdown-Menü für Einheitenkategorie.
        """
        category_dropdown.set("")
        source_unit_dropdown.set("")
        target_unit_dropdown.set("")

    def update_unit_dropdowns(self, category_dropdown, source_unit_dropdown, target_unit_dropdown):
        """
        Aktualisiert die Dropdown-Menüs für Quelleinheit und Zieleinheit basierend auf der Auswahl in der Einheitenkategorie.

        Args:
            category_dropdown (ttk.Combobox): Das Dropdown-Menü für Einheitenkategorie.
            source_unit_dropdown (ttk.Combobox): Das Dropdown-Menü für Quelleinheit.
            target_unit_dropdown (ttk.Combobox): Das Dropdown-Menü für Zieleinheit.
        """
        selected_category = category_dropdown.get()
        if selected_category:
            units = self.unit_categories[selected_category]
            source_unit_dropdown["values"] = units
            target_unit_dropdown["values"] = units
            source_unit_dropdown.set("")
            target_unit_dropdown.set("")  

    def transform_selected_parameters_to_dict(self):
        """
        Transformiert die ausgewählten Parameter in ein Wörterbuch.

        Returns:
            dict: Ein Wörterbuch, das die ausgewählten Parameter und ihre Einheiten enthält.
        """
        selected_parameters = {}
        for row_widgets in self.rows:
            pset_dropdown, param_dropdown, category_unit, source_unit, target_unit, _ = row_widgets
            if pset_dropdown.get() and param_dropdown.get() and source_unit.get() and target_unit.get():
                pset_name = pset_dropdown.get()
                param_name = param_dropdown.get()
                category_name = category_unit.get()
                source_unit_name = source_unit.get()
                target_unit_name = target_unit.get()
                selected_parameters[f"{pset_name} — {param_name} — {category_name}"] = {
                    "source_unit": source_unit_name,
                    "target_unit": target_unit_name
                }
        print(selected_parameters)
        return selected_parameters

    def erstellen_aktion(self):
        """
        Führt die Aktion zum Erstellen eines Templates aus und gibt die ausgewählten Informationen zurück.
        """
        if self.erstellen_button:
            name_template = self.name_template_entry.get()
            bearbeitet_durch = self.bearbeitet_durch_entry.get()
            beschreibung_template = self.beschreibung_template_entry.get()
            selected_parameters = self.transform_selected_parameters_to_dict()

            # Hier wird die Methode erstellen_template_callback aus main.py aufgerufen
            self.container.erstellen_template_callback(name_template, bearbeitet_durch, beschreibung_template, selected_parameters)
            
            if __name__ == "__main__":
                print("Name des Templates:", name_template)
                print("Zuletzt bearbeitet durch:", bearbeitet_durch)
                print("Beschreibung des Templates:", beschreibung_template)
                print("Ausgewählte Parameter für das Template:", selected_parameters)
            
            return name_template, bearbeitet_durch, beschreibung_template, selected_parameters

    def abbrechen_aktion(self):
        """
        Führt die Aktion zum Abbrechen des Vorgangs aus.
        """
        if self.abbrechen_aktion:
            self.container.abbrechen_template_callback()

if __name__ == "__main__":
    root = ctk.CTk()

    # Konfiguration der Fenstergröße und Position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = (3 * screen_width) // 4
    window_height = (2 * screen_height) // 3
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Beispieldaten für die Initialisierung Ihrer Klasse
    template_data = {
        "template_name": "test_2",
        "last_modified": "2023-12-18 20:31:28",
        "modified_by": "adsf",
        "description": "asdf",
        "parameters": {
            "Pset MEP — Calc-Pressure loss (Pa) — Druck": {
                "source_unit": "bar",
                "target_unit": "pascal"
            },
            "Pset MEP — Calc-Volumetric flow (m3/h) — Volumenstrom": {
                "source_unit": "meter**3/hour",
                "target_unit": "meter**3/second"
            },
            "Pset MEP — Tech-Weight (kg) — Masse": {
                "source_unit": "gram",
                "target_unit": "kilogram"
            }
        }
    }

    parameter_dict = {
        # Ihre Parameterdaten...
    }
    
    # Instanziieren und Anzeigen Ihres Frames
    frame = Neu_template_frame(root, window_width, window_height, template_data, parameter_dict)
    frame.pack(fill="both", expand=True)

    # Starten des Event-Loops
    root.mainloop()