# External Modules

# Internal Modules
## GUI
from GUI.main_windows.file_selector_frame import file_selector_frame as fsf
from GUI.status_windows.file_selector_status_frame import file_selctor_status_frame as fssf
from GUI.status_windows.unit_status_frame import unit_status_frame as usf
import GUI_main

## IFC operation
from IFC_operation.file_reader import modules_ifc_operation as modules

# Used Variables
VAR_FILEPATH = None

# Instanzieren von file_selector_frame mit Callback
window_import = fsf(GUI_main.ifc_import_callback)
window_import.mainloop()

# Überprüfen, ob der Import erfolgreich war
# VAR_FILEPATH = window_import.selected_file_path
# if VAR_FILEPATH:
#     file_imported = GUI_main.ifc_import_callback(VAR_FILEPATH)

# Hier können weitere Aktionen erfolgen, nachdem das File erfolgreich importiert wurde
