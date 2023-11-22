
from IFC_operation.file_reader import modules_ifc_operation as modules # Check if IFC is corrupted
from GUI.status_windows.file_selector_status_frame import file_selctor_status_frame as fssf # File unsuccessfully imported
from GUI.status_windows.unit_status_frame import unit_status_frame as usf # File successfully imported



# Callback-Funktion für IFC-Import
def ifc_import_callback(filepath):
    if modules.is_ifc_file(filepath):
        # Öffnet das Statusfenster für erfolgreichen Import
        window_unit_status = usf("SI")  # Ersetzen mit der effektiven Variable
        window_unit_status.mainloop()
        print("System Message:\tFile imported")
        return True
    else:
        # Öffnet das Statusfenster für fehlgeschlagenen Import
        window_import_status = fssf()
        window_import_status.mainloop()
        print("System Message:\tError Message")
        return False
    