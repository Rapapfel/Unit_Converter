import customtkinter as ctk
from GUI.main_windows.file_selector_frame import file_selector_frame as fsf
from IFC_operation.file_reader import modules_ifc_operation as modules
from GUI.status_windows.file_selector_status_frame import file_selctor_status_frame as fssf
from GUI.status_windows.unit_status_frame import unit_status_frame as usf
from GUI.main_windows.unit_selector_frame import Unit_selector as us
from GUI.template_windows.template_frame import BenutzerdefinierteVorlagen as bv
from GUI.template_windows.neu_template_frame import Neu_template_frame as ntf
from GUI.template_windows.bearbeiten_template_frame import bearbeiten_template_frame as btf
from GUI.template_windows.löschen_template_frame import DeleteTemplateConfirmation as dtcf
from GUI.template_windows.export_template_frame import ExportTemplateWindow as etw
from GUI.status_windows.export_template_status_frame import export_template_status_frame as estf
from GUI.template_windows.import_template_frame import ImportTemplateWindow as itw
from IFC_operation.template_handling import ifc_template_handler as ith
from GUI.main_windows.file_saver_frame import IFC_File_Saver_frame as ifsf
from GUI.status_windows.end_status_frame import end_status_frame as esf

class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("Logo.ico")
        # Screen Size, Windows size and position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = (3 * screen_width) // 4
        window_height = (2 * screen_height) // 3
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.title("Unit Converter")
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.current_frame = None
        self.parameter_dict = {}
        self.template_name = None

        # File selector Frame
        self.X = window_width - 10
        self.Y = window_height
        self.fsf = fsf(self,self.X,self.Y)
        self.frame_selection(self.fsf)

    def frame_selection(self, frame):
        if self.current_frame is not None:
            self.current_frame.place_forget()
        
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = frame
    
    def ifc_import_callback(self, VAR_FILEPATH):
        if modules.is_ifc_file(VAR_FILEPATH):
            window_unit_status = usf(self, "diversen Einheiten")
            window_unit_status.mainloop()
            self.parameter_dict = modules.extract_pset_parameters(VAR_FILEPATH)  # Erstelle parameter_dict hier
            self.frame_selection(us(self, self.X, self.Y))
            self.VAR_FILEPATH = VAR_FILEPATH
            return True, VAR_FILEPATH
        else:
            window_import_status = fssf()
            window_import_status.mainloop()
            return False

    def unit_selector_callback(self):
        self.frame_selection(bv(self, self.X, self.Y))

    def neu_template_frame_callback(self):
        self.frame_selection(ntf(self, self.X, self.Y, self.parameter_dict))
    
    def bearbeiten_template_frame_callback(self,template_data):
        bearbeiten_frame = btf(self, self.X, self.Y, template_data, self.parameter_dict)
        self.frame_selection(bearbeiten_frame)

    def abbrechen_template_callback(self):
        self.frame_selection(bv(self, self.X, self.Y))

    def erstellen_template_callback(self, name_template, bearbeitet_durch, beschreibung_template, selected_parameters):       
        ith.create_json_file(name_template, bearbeitet_durch, beschreibung_template, selected_parameters)
        self.frame_selection(bv(self, self.X, self.Y))
    
    def ändern_template_callback(self, template_data):
        # Extrahieren Sie die benötigten Daten aus template_data
        template_name_old = self.template_name  # Der Name des zu ändernden Templates
        template_name_new = template_data["template_name_new"]
        modified_by = template_data["modified_by"]
        description = template_data["description"]
        parameters = template_data["parameters"]

        # Rufen Sie die Methode zum Überschreiben der JSON-Datei auf
        ith.overwrite_json_file(template_name_old, template_name_new, modified_by, description, parameters)

        # Wechseln Sie zurück zur Template-Übersicht
        self.frame_selection(bv(self, self.X, self.Y))

    def set_current_template_name(self, template_name):
        self.template_name = template_name
    
    def löschen_template_frame_callback(self, template_name):
        dtcf(self, template_name, self)
    
    def yes_löschen_template_callback(self, template_name):
        ith.remove_json_file(template_name)
        self.frame_selection(bv(self, self.X, self.Y))
    
    def export_template_frame_callback(self, template_name):
        self.frame_selection(etw(self, self.X, self.Y, template_name))
    
    def process_export_template_frame(self, template_name, export_file_path):
        ith.export_json_file(template_name, export_file_path)
        estf(self, self)

    def export_template_status_frame_callback(self):
        self.frame_selection(bv(self, self.X, self.Y))
    
    def export_template_abbrechen_callback(self):
        self.frame_selection(bv(self, self.X, self.Y))
    
    def import_template_frame_callback(self):
        self.frame_selection(itw(self, self.X, self.Y))
    
    def process_import_template_frame(self, import_file_path):
        ith.import_json_file(import_file_path)
        self.frame_selection(bv(self, self.X, self.Y))
    
    def import_template_abbrechen_callback(self):
        self.frame_selection(bv(self, self.X, self.Y))

    def process_selected_template (self,template_name):
        print("template_name", template_name)
        self.template_name = template_name

    def file_saver_frame_callback (self):
        self.frame_selection(ifsf(self, self.X, self.Y))
    
    def process_selected_save_file_path (self, selected_save_file_path):
        print (selected_save_file_path)
        self.selected_save_file_path = selected_save_file_path

    def extract_data_and_update_ifc_callback(self):
        modules.extract_data_and_update_ifc(self.VAR_FILEPATH, self.selected_save_file_path, self.template_name)

    def end_status_frame_callback (self):
        self.frame_selection(esf(self, self.X, self.Y))

    def abbrechen(self):
        self.destroy()

if __name__ == "__main__":
    app = Window()
    app.mainloop()