import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class Neu_template_frame(ctk.CTkFrame):
    def __init__(self, container, parameter_dict):
        self.fg_color = "#242424"
        super().__init__(container, width=800, height=600, fg_color=self.fg_color)
        self.container = container
        self.parameter_dict = parameter_dict

        # Stil für ttk Widgets konfigurieren
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.fg_color, background=self.fg_color, foreground="white", arrowcolor="white")
        style.map("TCombobox", fieldbackground=[("readonly", self.fg_color)], selectbackground=[("readonly", self.fg_color)], selectforeground=[("readonly", "white")])

        # Container Frame für das Raster und den Scrollbar
        self.container_frame = ctk.CTkFrame(self, fg_color=self.fg_color)
        self.container_frame.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.4, anchor=ctk.W)  # Änderung: Verschiebung nach unten

        # Canvas für Scrollbar-Funktionalität
        self.canvas = tk.Canvas(self.container_frame, bg=self.fg_color, highlightthickness=0)  # Änderung: Rahmenfarbe entfernt
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar hinzufügen
        self.scrollbar = ctk.CTkScrollbar(self.container_frame, command=self.canvas.yview, fg_color=self.fg_color)  # Änderung: Rahmenfarbe gesetzt
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame für das Raster in den Canvas einbetten
        self.grid_frame = ctk.CTkFrame(self.canvas, fg_color=self.fg_color)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        # Listen zur Speicherung der Widgets
        self.rows = []  # Jede Zeile ist eine Liste von Widgets

        # Titel für die Spalten hinzufügen
        self.add_column_titles()

        # Button "+" zum Hinzufügen einer weiteren Zeile
        self.add_row_button = ctk.CTkButton(self, text="+", command=self.add_row)
        self.add_row_button.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

        # Button "Abbrechen" zum Hinzufügen
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen")
        self.cancel_button.place(relx=0.25, rely=0.85, anchor=ctk.CENTER)

        # Button "Template erstellen" zum Hinzufügen
        self.erstellen_button = ctk.CTkButton(self, text="Template erstellen")
        self.erstellen_button.place(relx=0.75, rely=0.85, anchor=ctk.CENTER)

        # Füge oben drei Eingabezeilen hinzu
        self.add_info_entries()

        # Scrollen mit dem Mausrad ermöglichen
        self.canvas.bind_all("<MouseWheel>", lambda event, canvas=self.canvas: self.scroll_canvas_area(event, canvas))

        self.canvas.bind("<Enter>", lambda event, canvas=self.canvas: canvas.bind_all("<MouseWheel>", lambda event, canvas=self.canvas: self.scroll_canvas_area(event, canvas)))
        self.canvas.bind("<Leave>", lambda event, canvas=self.canvas: canvas.unbind_all("<MouseWheel>"))

        # Füge beim Start eine Zeile hinzu
        self.add_row()

    def add_column_titles(self):
        titles = ["Pset", "Parameter", "Quelleinheit", "Zieleinheit"]
        for i, title in enumerate(titles):
            label = ctk.CTkLabel(self.grid_frame, text=title, fg_color=self.fg_color)
            label.grid(row=0, column=i, sticky="nsew")
            
            # Ändern Sie die Breite der "Parameter"-Spalte
            if title == "Parameter":
                self.grid_frame.grid_columnconfigure(i, minsize=220)  # Passen Sie die Breite nach Bedarf an

    def add_info_entries(self):
        info_labels = ["Name des Templates:", "Zuletzt bearbeitet durch:", "Beschreibung:"]
        for i, label_text in enumerate(info_labels):
            label = ctk.CTkLabel(self, text=label_text, fg_color=self.fg_color)
            label.place(relx=0.1, rely=0.1 + i * 0.05, anchor=ctk.W)
            entry = tk.Entry(self, background=self.fg_color, foreground="white")
            entry.place(relx=0.3, rely=0.1 + i * 0.05, relwidth=0.6)

    def add_row(self):
        if not self.rows or all(self.is_row_complete(row) for row in self.rows):
            row_index = len(self.rows) + 1
            widgets = self.create_row_widgets(row_index)
            self.rows.append(widgets)
            self.update_scrollregion()

    def create_row_widgets(self, row_index):
        widgets = []

        # Erstellen und Platzieren von Widgets für die neue Zeile
        pset_var = tk.StringVar()
        pset_dropdown = ttk.Combobox(self.grid_frame, textvariable=pset_var, values=list(self.parameter_dict.keys()), state="readonly", style="TCombobox")
        pset_dropdown.grid(row=row_index, column=0, sticky="nsew")
        widgets.append(pset_dropdown)

        param_var = tk.StringVar()
        param_dropdown = ttk.Combobox(self.grid_frame, textvariable=param_var, state="readonly", style="TCombobox")
        param_dropdown.grid(row=row_index, column=1, sticky="nsew")
        widgets.append(param_dropdown)

        source_unit = tk.Entry(self.grid_frame, background=self.fg_color, foreground="white", justify="center")  # Text in der Mitte ausrichten
        source_unit.grid(row=row_index, column=2, sticky="nsew")
        widgets.append(source_unit)

        target_unit = tk.Entry(self.grid_frame, background=self.fg_color, foreground="white", justify="center")  # Text in der Mitte ausrichten
        target_unit.grid(row=row_index, column=3, sticky="nsew")
        widgets.append(target_unit)

        remove_button = ctk.CTkButton(self.grid_frame, text="-", width=2, height=1, command=lambda: self.remove_row(row_index))
        remove_button.grid(row=row_index, column=4, sticky="nsew")
        widgets.append(remove_button)

        pset_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_param_dropdown(event, pset_dropdown, param_dropdown))

        return widgets

    def is_row_complete(self, row_widgets):
        return all(widget.get() != "" for widget in row_widgets[:3])

    def update_param_dropdown(self, event, pset_dropdown, param_dropdown):
        selected_pset = pset_dropdown.get()
        param_dropdown["values"] = self.parameter_dict.get(selected_pset, [])
        param_dropdown.set("")

    def remove_row(self, row_index):
        for widget in self.rows[row_index - 1]:
            widget.grid_forget()
        self.rows.pop(row_index - 1)
        self.reorganize_rows()
        self.update_scrollregion()

    def reorganize_rows(self):
        for i, row_widgets in enumerate(self.rows, start=1):
            for j, widget in enumerate(row_widgets):
                widget.grid(row=i, column=j, sticky="nsew")

    def update_scrollregion(self):
        self.grid_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def scroll_canvas_area(self, event, canvas):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

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
