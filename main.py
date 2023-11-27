# External Modules

# Internal Modules
## GUI
from GUI.main_windows.file_selector_frame import file_selector_frame as fsf
import GUI_main

## IFC operation

# Used Variables
VAR_FILEPATH = None

# Instanzieren von file_selector_frame mit Callback
window_import = fsf(GUI_main.ifc_import_callback)
window_import.mainloop()
