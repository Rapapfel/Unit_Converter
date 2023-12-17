import customtkinter as ctk
from GUI.main_windows.file_selector_frame import file_selector_frame as fsf
from IFC_operation.file_reader import modules_ifc_operation as modules
from GUI.status_windows.file_selector_status_frame import file_selctor_status_frame as fssf
from GUI.status_windows.unit_status_frame import unit_status_frame as usf
from GUI.main_windows.unit_selector_frame import Unit_selector
from GUI.template_windows.template_frame import BenutzerdefinierteVorlagen as bv
from GUI.template_windows.neu_template_frame import Neu_template_frame as ntf
from IFC_operation.template_handling import ifc_template_handler as ith

class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Screen Size, Windows size and position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.title("Einheitenaustausch")
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.current_frame = None
        self.parameter_dict = {}

        # File selector Frame
        X = window_width - 60
        Y = window_height
        self.fsf = fsf(self,X,Y)
        self.frame_selection(self.fsf)
        print("Fertig")

    def frame_selection(self, frame):
        if self.current_frame is not None:
            self.current_frame.place_forget()
        
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = frame
    
    def ifc_import_callback(self, VAR_FILEPATH):
        if modules.is_ifc_file(VAR_FILEPATH):
            window_unit_status = usf(self, "diversen Einheiten")
            window_unit_status.mainloop()
            print("Systemnachricht:\tDatei importiert")
            self.parameter_dict = modules.extract_pset_parameters(VAR_FILEPATH)  # Erstelle parameter_dict hier
            self.frame_selection(Unit_selector(self))
            self.VAR_FILEPATH = VAR_FILEPATH
            return True, VAR_FILEPATH
        else:
            window_import_status = fssf()
            window_import_status.mainloop()
            print("Systemnachricht:\tFehlermeldung")
            return False

    def unit_selector_callback(self):
        self.frame_selection(bv(self))

    def neu_template_frame_callback(self):
        self.frame_selection(ntf(self, self.parameter_dict))

    def abbrechen_template_callback(self):
        self.frame_selection(bv(self))

    def erstellen_template_callback(self, name_template, bearbeitet_durch, beschreibung_template, selected_parameters):
        
        # Führen Sie hier den gewünschten Code aus, um die Parameter auszudrucken
        print("Name des Templates:", name_template)
        print("Zuletzt bearbeitet durch:", bearbeitet_durch)
        print("Beschreibung des Templates:", beschreibung_template)
        print("Ausgewählte Parameter für das Template:", selected_parameters)
        
        ith.create_json_file(name_template, bearbeitet_durch, beschreibung_template, selected_parameters)

        self.frame_selection(bv(self))
    
    def process_selected_template (self,template_name):
        print(template_name)
        return template_name

    def extract_data_and_update_ifc_callback(self, template_name):
        modules.extract_data_and_update_ifc(self.VAR_FILEPATH, template_name)

    def abbrechen(self):
        self.destroy()

if __name__ == "__main__":
    app = Window()
    app.mainloop()
