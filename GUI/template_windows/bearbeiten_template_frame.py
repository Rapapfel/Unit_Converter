import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
import json

class bearbeiten_template_frame(ctk.CTkFrame):
    def __init__(self, container, X, Y, template_data, parameter_dict):
        """
        Initialisiert das Template-Bearbeitungs-Fenster.

        Args:
            container (objekt): Das übergeordnete Container-Objekt.
            X (int): Breite des Frames.
            Y (int): Höhe des Frames.
            template_data (dict): Daten des Templates, z.B. Name, Beschreibung, Parameter.
            parameter_dict (dict): Dictionary mit verfügbaren Parametern.
        """
        # Hintergrundfarbe für das Fenster
        self.fg_color = "#242424"
        super().__init__(container, width=X, height=Y, fg_color=self.fg_color)
        self.container = container
        self.parameter_dict = parameter_dict
        self.template_parameter_dict = template_data.get("parameters", {})
        self.font_size = ("Arial", 18)
        self.option_add('*TCombobox*Font', ('Arial', 15))

        # Vorbefüllen der allgemeinen Template-Informationen
        self.name_template = template_data.get("template_name", "")
        self.bearbeitet_durch = template_data.get("modified_by", "")
        self.beschreibung_template = template_data.get("description", "")

        # Laden der Einheiten aus der JSON-Datei
        current_script = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_script, "..","..","IFC_operation\\units\\units.json")
        with open(json_path, "r") as file:
            self.unit_categories = json.load(file)

        # Erzeugung des GUI-Stils
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.fg_color, background=self.fg_color, foreground="white", arrowcolor="white")
        style.map("TCombobox", fieldbackground=[("readonly", self.fg_color)], selectbackground=[("readonly", self.fg_color)], selectforeground=[("readonly", "white")])

        # Erzeugung des Container-Frames
        self.container_frame = ctk.CTkFrame(self, fg_color=self.fg_color)
        self.container_frame.place(relx=0.1, rely=0.5, relwidth=0.9, relheight=0.4, anchor=ctk.W)

        # Erzeugung der Canvas für das Scrollen
        self.canvas = tk.Canvas(self.container_frame, bg=self.fg_color, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Erzeugung der Scrollleiste
        self.scrollbar = ctk.CTkScrollbar(self.container_frame, command=self.canvas.yview, fg_color=self.fg_color)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Erzeugung des Gitter-Frames im Canvas
        self.grid_frame = ctk.CTkFrame(self.canvas, fg_color=self.fg_color)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        # Liste für die Zeilen im Grid
        self.rows = []

        # Hinzufügen der Spaltentitel
        self.add_column_titles()

        # Hinzufügen der "+""-Schaltfläche für neue Zeilen
        self.add_row_button = ctk.CTkButton(self, text="+", command=self.add_row)
        self.add_row_button.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

         # Button "Abbrechen" zum Hinzufügen
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.abbrechen_aktion)
        self.cancel_button.place(relx=0.25, rely=0.85, anchor=ctk.CENTER)

        # Button "Template ändern" zum Ändern
        self.ändern_button = ctk.CTkButton(self, text="Template ändern", command=self.ändern_aktion)
        self.ändern_button.place(relx=0.75, rely=0.85, anchor=ctk.CENTER)

         # Zusätzliche Eingabefelder für Template-Informationen
        self.name_template_entry = tk.Entry(self, background=self.fg_color, foreground="white", font=self.font_size)
        self.name_template_entry.place(relx=0.3, rely=0.1, relwidth=0.6)
        self.bearbeitet_durch_entry = tk.Entry(self, background=self.fg_color, foreground="white", font=self.font_size)
        self.bearbeitet_durch_entry.place(relx=0.3, rely=0.15, relwidth=0.6)
        self.beschreibung_template_entry = tk.Entry(self, background=self.fg_color, foreground="white", font=self.font_size)
        self.beschreibung_template_entry.place(relx=0.3, rely=0.2, relwidth=0.6)

        # Hinzufügen von Info-Etiketten für die Template-Informationen
        self.add_info_entries()

        # Hinzufügen einer leeren Zeile, wenn keine Parameter vorhanden sind
        if len(self.template_parameter_dict.items()) == 0:
            self.add_row()

        # Füllen Sie die Eingabefelder mit den Daten
        self.name_template_entry.insert(0, self.name_template)
        self.bearbeitet_durch_entry.insert(0, self.bearbeitet_durch)
        self.beschreibung_template_entry.insert(0, self.beschreibung_template)

        # Vorbelegen der Parameterzeilen
        self.initialize_parameters()

    def initialize_parameters(self):
        """
        Initialisiert die Parameter auf Basis eines Vorlagenparameter-Dikts.
        """
        for param_key, param_values in self.template_parameter_dict.items():
            # Zerlege den zusammengesetzten Schlüssel
            pset_name, param_name, category_name = param_key.split(' — ')
            full_param_info = {
                "pset_name": pset_name,
                "param_name": param_name,
                "category_name": category_name,
                **param_values
            }
            self.add_row(full_param_info)

    def add_column_titles(self):
        """
        Fügt Spaltentitel zur Benutzeroberfläche hinzu.
        """
        titles = ["Pset", "Parameter", "Einheitenkategorie", "Quelleinheit", "Zieleinheit", ""]
        column_widths = [100, 220, 150, 200, 200, 20]  # Definiert die Spaltenbreiten
        row_height = 30  # Beispielhöhe, kann angepasst werden
        for i, (title, width) in enumerate(zip(titles, column_widths)):
            label = ctk.CTkLabel(self.grid_frame, text=title, fg_color=self.fg_color, width=width, height=row_height)
            label.grid(row=0, column=i, sticky="nsew")
            if title == "Parameter":
                self.grid_frame.grid_columnconfigure(i, minsize=220)

    def add_info_entries(self):
        """
        Fügt Informationslabels zur Benutzeroberfläche hinzu.
        """
        info_labels = ["Name des Templates:", "Zuletzt bearbeitet durch:", "Beschreibung:"]
        for i, label_text in enumerate(info_labels):
            label = ctk.CTkLabel(self, text=label_text, fg_color=self.fg_color)
            label.place(relx=0.1, rely=0.1 + i * 0.05, anchor=ctk.W)

    def add_row(self, param_info=None):
        """
        Fügt eine Zeile zur Tabelle hinzu.
        """
        row_index = len(self.rows) + 1
        widgets = self.create_row_widgets(row_index, param_info)
        self.rows.append(widgets)
        self.update_scrollregion()

    def create_row_widgets(self, row_index, param_info=None):
        """
        Erstellt die Widgets für eine Zeile in der Tabelle.
        """
        widgets = []

        # Dropdown für Pset
        pset_var = tk.StringVar()
        pset_dropdown = ttk.Combobox(self.grid_frame, textvariable=pset_var, values=list(self.parameter_dict.keys()), state="readonly", style="TCombobox", font=self.font_size)
        pset_dropdown.grid(row=row_index, column=0, sticky="nsew")
        widgets.append(pset_dropdown)

        # Dropdown für Parameter
        param_var = tk.StringVar()
        param_dropdown = ttk.Combobox(self.grid_frame, textvariable=param_var, state="readonly", style="TCombobox", font= self.font_size)
        param_dropdown.grid(row=row_index, column=1, sticky="nsew")
        widgets.append(param_dropdown)

        # Dropdown für Einheitenkategorie
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(self.grid_frame, textvariable=category_var, values=list(self.unit_categories.keys()), state="readonly", style="TCombobox", font=self.font_size)
        category_dropdown.grid(row=row_index, column=2, sticky="nsew")
        widgets.append(category_dropdown)

        # Dropdown für Quelleinheit
        source_unit_var = tk.StringVar()
        source_unit_dropdown = ttk.Combobox(self.grid_frame, textvariable=source_unit_var, state="readonly", style="TCombobox", font=self.font_size)
        source_unit_dropdown.grid(row=row_index, column=3, sticky="nsew")
        widgets.append(source_unit_dropdown)

        # Dropdown für Zieleinheit
        target_unit_var = tk.StringVar()
        target_unit_dropdown = ttk.Combobox(self.grid_frame, textvariable=target_unit_var, state="readonly", style="TCombobox", font=self.font_size)
        target_unit_dropdown.grid(row=row_index, column=4, sticky="nsew")
        widgets.append(target_unit_dropdown)

        # Entfernen-Button
        remove_button = ctk.CTkButton(self.grid_frame, text="-", width=2, height=1, command=lambda: self.remove_row(row_index))
        remove_button.grid(row=row_index, column=5, sticky="nsew")
        widgets.append(remove_button)

        # Event-Handler für Dropdown-Auswahl
        pset_dropdown.bind("<<ComboboxSelected>>", lambda event, pset_dropdown=pset_dropdown, param_dropdown=param_dropdown: self.update_pset_dropdown(pset_dropdown, param_dropdown, source_unit_dropdown, target_unit_dropdown, category_dropdown))
        param_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_param_dropdown(source_unit_dropdown, target_unit_dropdown, category_dropdown))
        category_dropdown.bind("<<ComboboxSelected>>", lambda event, source_unit_dropdown=source_unit_dropdown, target_unit_dropdown=target_unit_dropdown: self.update_unit_dropdowns(category_dropdown, source_unit_dropdown, target_unit_dropdown))

        # Initialisiere Dropdown-Texte
        pset_dropdown["text"]=""
        param_dropdown["text"]=""
        category_dropdown["text"]=""
        source_unit_dropdown["text"]=""
        target_unit_dropdown["text"]=""
        
        # Setze Dropdown-Werte basierend auf param_info
        if param_info:
            pset_dropdown.set(param_info.get("pset_name", ""))
            self.update_pset_dropdown(pset_dropdown, param_dropdown, source_unit_dropdown, target_unit_dropdown, category_dropdown)
            param_dropdown.set(param_info.get("param_name", ""))
            category_dropdown.set(param_info.get("category_name", ""))
            self.update_unit_dropdowns(category_dropdown, source_unit_dropdown, target_unit_dropdown)
            source_unit_dropdown.set(param_info.get("source_unit", ""))
            target_unit_dropdown.set(param_info.get("target_unit", ""))

        return widgets

    def update_scrollregion(self):
        """
        Aktualisiert die Scrollregion des Canvas.
        """
        self.grid_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

def scroll_canvas_area(self, event, canvas):
    """
    Scrollt den Bereich der Leinwand basierend auf dem Mausradereignis.

    Args:
        event (Event): Das Mausradereignis.
        canvas (Canvas): Die Leinwand, die gescrollt werden soll.
    """
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def is_row_complete(self, row_widgets):
    """
    Überprüft, ob alle Widgets in einer Zeile einen ausgewählten Wert haben.

    Args:
        row_widgets (Tuple): Die Widgets in der Zeile.

    Returns:
        bool: True, wenn alle Widgets einen ausgewählten Wert haben, sonst False.
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
    Aktualisiert das Parameter-Set Dropdown basierend auf dem ausgewählten Wert der vorherigen Dropdowns.

    Args:
        pset_dropdown (Dropdown): Das Dropdown für das Parameter-Set.
        param_dropdown (Dropdown): Das Dropdown für die Parameter.
        source_unit_dropdown (Dropdown): Das Dropdown für die Quelleinheit.
        target_unit_dropdown (Dropdown): Das Dropdown für die Zieleinheit.
        category_dropdown (Dropdown): Das Dropdown für die Kategorie.
    """
    selected_pset = pset_dropdown.get()
    param_dropdown["values"] = self.parameter_dict[selected_pset]
    param_dropdown.set("")
    category_dropdown.set("")
    source_unit_dropdown.set("")
    target_unit_dropdown.set("")

def update_param_dropdown(self, source_unit_dropdown, target_unit_dropdown, category_dropdown):
    """
    Aktualisiert das Parameter-Dropdown basierend auf dem ausgewählten Wert des Kategorien-Dropdowns.

    Args:
        source_unit_dropdown (Dropdown): Das Dropdown für die Quelleinheit.
        target_unit_dropdown (Dropdown): Das Dropdown für die Zieleinheit.
        category_dropdown (Dropdown): Das Dropdown für die Kategorie.
    """
    category_dropdown.set("")
    source_unit_dropdown.set("")
    target_unit_dropdown.set("")

def update_unit_dropdowns(self, category_dropdown, source_unit_dropdown, target_unit_dropdown):
    """
    Aktualisiert die Quell- und Zieleinheit-Dropdowns basierend auf dem ausgewählten Wert des Kategorien-Dropdowns.

    Args:
        category_dropdown (Dropdown): Das Dropdown für die Kategorie.
        source_unit_dropdown (Dropdown): Das Dropdown für die Quelleinheit.
        target_unit_dropdown (Dropdown): Das Dropdown für die Zieleinheit.
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
    Wandelt die ausgewählten Parameter in ein Wörterbuch um.

    Returns:
        dict: Das Wörterbuch der ausgewählten Parameter.
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
    return selected_parameters

def ändern_aktion(self):
    """
    Führt die Aktion der Template-Änderung basierend auf den eingegebenen Werten aus.
    """
    if self.ändern_button:
        name_template_neu = self.name_template_entry.get()
        bearbeitet_durch = self.bearbeitet_durch_entry.get()
        beschreibung_template = self.beschreibung_template_entry.get()
        selected_parameters = self.transform_selected_parameters_to_dict()

        template_data = {
            "template_name_new": name_template_neu,
            "modified_by": bearbeitet_durch,
            "description": beschreibung_template,
            "parameters": selected_parameters
        }

        self.container.ändern_template_callback(template_data)

def abbrechen_aktion(self):
    """
    Führt die Aktion der Template-Abbruch aus.
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

    parameter_dict = {'Pset MEP': ['Abbreviation', 'Calc-Pressure loss (Pa)', 'Calc-Required throttling (Pa)', 'Calc-Volumetric flow (m3/h)', 'Calc-Zeta', 'Geom-Additional length (mm)', 'Geom-Angle (°)', 'Geom-Branch length (mm)', 'Geom-Connection length (mm)', 'Geom-Connection Ø (mm)', 'Geom-DN', 'Geom-DN1', 'Geom-DN2', 'Geom-DN3', 'Geom-Half length (mm)', 'Geom-Head Ø (mm)', 'Geom-Housing length (mm)', 'Geom-Housing Ø (mm)', 'Geom-Length (mm)', 'Geom-Length 1 (mm)', 'Geom-Length 2 (mm)', 'Geom-Length branch (mm)', 'Geom-Length outlet (mm)', 'Geom-Main side (mm)', 'Geom-Offnet (mm)', 'Geom-Offset (mm)', 'Geom-Offset 1 (mm)', 'Geom-Offset 2 (mm)', 'Geom-Offset to edge 1 (mm)', 'Geom-Offset to edge 2 (mm)', 'Geom-Outer Ø (mm)', 'Geom-Outer Ø1 (mm)', 'Geom-Outer Ø2 (mm)', 'Geom-Outer Ø3 (mm)', 'Geom-Radius (mm)', 'Geom-Secondary side 1 (mm)', 'Geom-Secondary side 2 (mm)', 'Geom-Section 1 side 1 (mm)', 'Geom-Section 1 side 2 (mm)', 'Geom-Section 2 side 1 (mm)', 'Geom-Section 2 side 2 (mm)', 'Geom-Segment number (if segmented)', 'Geom-Side 1 (mm)', 'Geom-Side 2 (mm)', 'Geom-Spacing between branches (mm)', 'Geom-Spacing to branch (mm)', 'Geom-Surface (m2)', 'Geom-Tenon (mm)', 'Geom-Thickness (mm)', 'Geom-Thickness(mm)', 'Geom-Ø (mm)', 'Geom-Ø branch  (mm)', 'Geom-Ø main (mm)', 'Geom-Ø secondary (mm)', 'Info', 'Name', 'Tech-Insulation surface (m2)', 'Tech-Insulation thickness (mm)', 'Tech-Material', 'Tech-Material (ID)', 'Tech-Medium', 'Tech-Weight (kg)'], 'Pset_SlabCommon': ['IsExternal', 'ThermalTransmittance'], 'Pset nova - Archi': ['Name']}
    
    # Instanziieren und Anzeigen Ihres Frames
    frame = bearbeiten_template_frame(root, window_width, window_height, template_data, parameter_dict)
    frame.pack(fill="both", expand=True)

    # Starten des Event-Loops
    root.mainloop()
