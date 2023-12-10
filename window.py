import customtkinter as ctk
from GUI.main_windows.file_selector_frame import file_selector_frame as fsf
from IFC_operation.file_reader import modules_ifc_operation as modules # Check if IFC is corrupted
from GUI.status_windows.file_selector_status_frame import file_selctor_status_frame as fssf # File unsuccessfully imported
from GUI.status_windows.unit_status_frame import unit_status_frame as usf # File successfully imported
from GUI.main_windows.unit_selector_frame import Unit_selector

class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Unit Changer")
        self.geometry("1000x500")
        self.current_frame = None

        self.fsf = fsf(self)
        self.frame_selection(self.fsf)
        print("finish")

    def frame_selection(self, frame):
        if self.current_frame != None:
            self.current_frame.place_forget()
        
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = frame
    
    # Callback-Funktion für IFC-Import
    def ifc_import_callback(self, filepath):
        if modules.is_ifc_file(filepath):
            # Öffnet das Statusfenster für erfolgreichen Import
            window_unit_status = usf("SI")  # Ersetzen mit der effektiven Variable
            window_unit_status.mainloop()
            print("System Message:\tFile imported")
            self.frame_selection(Unit_selector(self))
            return True
        else:
            # Öffnet das Statusfenster für fehlgeschlagenen Import
            window_import_status = fssf()
            window_import_status.mainloop()
            print("System Message:\tError Message")
            return False
    

    def abbrechen(self):
        self.destroy()
        




if __name__ == "__main__":
    app = Window()
    app.mainloop()