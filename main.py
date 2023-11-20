# External Modules
import customtkinter as ctk

# Internal Modules
## GUI
from GUI.main_windows.file_selector_frame import file_selector_frame as fsf
from GUI.status_windows.file_selector_status_frame import file_selctor_status_frame as fssf

## IFC operation
from IFC_operation.file_reader import modules_ifc_operation as modules

# Used Variables
window_import = fsf()
window_import_status = fssf()



VAR_FILEPATH = None

# As long as a Error occurs, input phase stays active
file_imported = False
while file_imported == False:

    window_import.mainloop()

    VAR_FILEPATH = window_import.selected_file_path

    # Validate Import
    if modules.is_ifc_file(VAR_FILEPATH) == True:
        file_imported = True
        print("System Message:\tFile imported")
    else:
        file_imported = False
        #window_import_status.mainloop()
        print("System Message:\tError Message")