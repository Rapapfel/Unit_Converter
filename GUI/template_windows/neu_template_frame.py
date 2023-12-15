import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import json

class Neu_template_frame(ctk.CTkFrame):
    def __init__(self, container, parameter_dict, name_template="", bearbeitet_durch="", beschreibung_template=""):
        self.fg_color = "#242424"
        super().__init__(container, width=1500, height=600, fg_color=self.fg_color)
        self.container = container
        self.parameter_dict = parameter_dict
        self.name_template = name_template
        self.bearbeitet_durch = bearbeitet_durch
        self.beschreibung_template = beschreibung_template

            # Laden der Einheiten aus der JSON-Datei
        with open(r"C:\Users\ragre\OneDrive - Hochschule Luzern\DC_Scripting\unit_changer\IFC_operation\units\units.json", "r") as file:
            self.unit_categories = json.load(file)  # Verwenden von self hier

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.fg_color, background=self.fg_color, foreground="white", arrowcolor="white")
        style.map("TCombobox", fieldbackground=[("readonly", self.fg_color)], selectbackground=[("readonly", self.fg_color)], selectforeground=[("readonly", "white")])

        self.container_frame = ctk.CTkFrame(self, fg_color=self.fg_color)
        self.container_frame.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.4, anchor=ctk.W)

        self.canvas = tk.Canvas(self.container_frame, bg=self.fg_color, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.container_frame, command=self.canvas.yview, fg_color=self.fg_color)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.grid_frame = ctk.CTkFrame(self.canvas, fg_color=self.fg_color)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        self.rows = []

        self.add_column_titles()

        self.add_row_button = ctk.CTkButton(self, text="+", command=self.add_row)
        self.add_row_button.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

         # Button "Abbrechen" zum Hinzufügen
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen")
        self.cancel_button.place(relx=0.25, rely=0.85, anchor=ctk.CENTER)

        # Button "Template erstellen" zum Hinzufügen
        self.erstellen_button = ctk.CTkButton(self, text="Template erstellen", command=self.erstellen_aktion)
        self.erstellen_button.place(relx=0.75, rely=0.85, anchor=ctk.CENTER)

         # Zusätzliche Eingabefelder für Template-Informationen
        self.name_template_entry = tk.Entry(self, background=self.fg_color, foreground="white")
        self.name_template_entry.place(relx=0.3, rely=0.1, relwidth=0.6)
        self.bearbeitet_durch_entry = tk.Entry(self, background=self.fg_color, foreground="white")
        self.bearbeitet_durch_entry.place(relx=0.3, rely=0.15, relwidth=0.6)
        self.beschreibung_template_entry = tk.Entry(self, background=self.fg_color, foreground="white")
        self.beschreibung_template_entry.place(relx=0.3, rely=0.2, relwidth=0.6)

        self.add_info_entries()

        self.add_row()

    def add_column_titles(self):
        titles = ["Pset", "Parameter", "Einheitenkategorie", "Quelleinheit", "Zieleinheit", ""]
        column_widths = [100, 220, 150, 300, 300, 40]  # Define column widths
        for i, (title, width) in enumerate(zip(titles, column_widths)):
            label = ctk.CTkLabel(self.grid_frame, text=title, fg_color=self.fg_color, width=width)
            label.grid(row=0, column=i, sticky="nsew")
            if title == "Parameter":
                self.grid_frame.grid_columnconfigure(i, minsize=220)

    def add_info_entries(self):
        info_labels = ["Name des Templates:", "Zuletzt bearbeitet durch:", "Beschreibung:"]
        for i, label_text in enumerate(info_labels):
            label = ctk.CTkLabel(self, text=label_text, fg_color=self.fg_color)
            label.place(relx=0.1, rely=0.1 + i * 0.05, anchor=ctk.W)

    def add_row(self):
        if not self.rows or all(self.is_row_complete(row) for row in self.rows):
            row_index = len(self.rows) + 1
            widgets = self.create_row_widgets(row_index)
            self.rows.append(widgets)
            self.update_scrollregion()

    def create_row_widgets(self, row_index):
        widgets = []

        pset_var = tk.StringVar()
        pset_dropdown = ttk.Combobox(self.grid_frame, textvariable=pset_var, values=list(self.parameter_dict.keys()), state="readonly", style="TCombobox")
        pset_dropdown.grid(row=row_index, column=0, sticky="nsew")
        widgets.append(pset_dropdown)

        param_var = tk.StringVar()
        param_dropdown = ttk.Combobox(self.grid_frame, textvariable=param_var, state="readonly", style="TCombobox")
        param_dropdown.grid(row=row_index, column=1, sticky="nsew")
        widgets.append(param_dropdown)

        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(self.grid_frame, textvariable=category_var, values=list(self.unit_categories.keys()), state="readonly", style="TCombobox")
        category_dropdown.grid(row=row_index, column=2, sticky="nsew")
        widgets.append(category_dropdown)

        source_unit_var = tk.StringVar()
        source_unit_dropdown = ttk.Combobox(self.grid_frame, textvariable=source_unit_var, state="readonly", style="TCombobox")
        source_unit_dropdown.grid(row=row_index, column=3, sticky="nsew")
        widgets.append(source_unit_dropdown)

        target_unit_var = tk.StringVar()
        target_unit_dropdown = ttk.Combobox(self.grid_frame, textvariable=target_unit_var, state="readonly", style="TCombobox")
        target_unit_dropdown.grid(row=row_index, column=4, sticky="nsew")
        widgets.append(target_unit_dropdown)

        remove_button = ctk.CTkButton(self.grid_frame, text="-", width=2, height=1, command=lambda: self.remove_row(row_index))
        remove_button.grid(row=row_index, column=5, sticky="nsew")
        widgets.append(remove_button)

        pset_dropdown.bind("<<ComboboxSelected>>", lambda event, pset_dropdown=pset_dropdown, param_dropdown=param_dropdown: self.update_param_dropdown(event, pset_dropdown, param_dropdown))
        category_dropdown.bind("<<ComboboxSelected>>", lambda event, row_index=row_index, source_unit_dropdown=source_unit_dropdown, target_unit_dropdown=target_unit_dropdown: self.update_unit_dropdowns(event, category_dropdown, source_unit_dropdown, target_unit_dropdown, row_index))

        return widgets

    def update_scrollregion(self):
        self.grid_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def scroll_canvas_area(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def is_row_complete(self, row_widgets):
        pset_dropdown, param_dropdown, category_dropdown, source_unit_dropdown, target_unit_dropdown, remove_button = row_widgets
        return pset_dropdown.get() and param_dropdown.get() and category_dropdown.get() and source_unit_dropdown.get() and target_unit_dropdown.get()

    def remove_row(self, row_index):
        widgets_to_remove = self.rows.pop(row_index - 1)
        for widget in widgets_to_remove:
            widget.destroy()
        self.update_scrollregion()

    def update_param_dropdown(self, event, pset_dropdown, param_dropdown):
        selected_pset = pset_dropdown.get()
        if selected_pset:
            param_dropdown["values"] = self.parameter_dict[selected_pset]
        else:
            param_dropdown.set("")

    def update_unit_dropdowns(self, event, category_dropdown, source_unit_dropdown, target_unit_dropdown, row_index):
        selected_category = category_dropdown.get()
        if selected_category:
            units = self.unit_categories[selected_category]
            source_unit_dropdown["values"] = units
            target_unit_dropdown["values"] = units
            source_unit_dropdown.set("")
            target_unit_dropdown.set("")
            source_unit_dropdown["state"] = "readonly"
            target_unit_dropdown["state"] = "readonly"
        else:
            source_unit_dropdown.set("")
            target_unit_dropdown.set("")
            source_unit_dropdown["state"] = "readonly"
            target_unit_dropdown["state"] = "readonly"
    

    def transform_selected_parameters_to_dict(self):
            selected_parameters = {}
            for row_widgets in self.rows:
                pset_dropdown, param_dropdown, category_unit, source_unit, target_unit, _ = row_widgets
                if pset_dropdown.get() and param_dropdown.get() and source_unit.get() and target_unit.get():
                    pset_name = pset_dropdown.get()
                    param_name = param_dropdown.get()
                    category_name = category_unit.get()
                    source_unit_name = source_unit.get()
                    target_unit_name = target_unit.get()
                    selected_parameters[f"{pset_name} - {param_name} - {category_name}"] = {
                        "source_unit": source_unit_name,
                        "target_unit": target_unit_name
                    }
            print(selected_parameters)
            return selected_parameters

    def erstellen_aktion(self):
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
        

if __name__ == "__main__":
    parameter_dict = {
        'Pset MEP': ['Abkürzung', 'Berechneter Druckverlust (Pa)', 'Berechnete erforderliche Drosselung (Pa)', 'Calc-Volumetric flow (m3/h)'],
        'Pset_SlabCommon': ['IstExtern', 'Wärmedurchgangskoeffizient'],
        'Pset nova - Archi': ['Name']
    }

    root = tk.Tk()
    root.title("Hauptfenster")

    app = Neu_template_frame(root, parameter_dict)
    app.pack(fill="both", expand=True)

    root.mainloop()