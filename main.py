import customtkinter as ctk
from GUI.main_windows.file_selector_frame import file_selector_frame as fsf
from IFC_operation.file_reader import modules_ifc_operation as modules
from GUI.status_windows.file_selector_status_frame import file_selctor_status_frame as fssf
from GUI.status_windows.unit_status_frame import unit_status_frame as usf
from GUI.main_windows.unit_selector_frame import Unit_selector
from GUI.template_windows.template_frame import BenutzerdefinierteVorlagen as bv
from GUI.template_windows.neu_template_frame import Neu_template_frame as ntf

class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Einheitenaustausch")
        self.geometry("2000x1000")
        self.current_frame = None
        self.parameter_dict = {}  # Initialisiere parameter_dict hier

        self.fsf = fsf(self)
        self.frame_selection(self.fsf)
        print("Fertig")

    def frame_selection(self, frame):
        if self.current_frame is not None:
            self.current_frame.place_forget()
        
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = frame
    
    def ifc_import_callback(self, filepath):
        if modules.is_ifc_file(filepath):
            window_unit_status = usf(self, "SI")
            window_unit_status.mainloop()
            print("Systemnachricht:\tDatei importiert")
            self.parameter_dict = modules.extract_pset_parameters(filepath)  # Erstelle parameter_dict hier
            self.frame_selection(Unit_selector(self))
            return True
        else:
            window_import_status = fssf()
            window_import_status.mainloop()
            print("Systemnachricht:\tFehlermeldung")
            return False
    
    def get_selected_file_path(self):
        return self.fsf.selected_file_path

    def unit_selector_callback(self):
        print("Ausgewählt")
        self.frame_selection(bv(self))

    def neu_template_frame_callback(self):
        self.frame_selection(ntf(self, self.parameter_dict))

    def erstellen_template_callback(self):
        self.erstellen_template_callback(bv(self))        

    def abbrechen(self):
        self.destroy()

if __name__ == "__main__":
    app = Window()
    app.mainloop()
