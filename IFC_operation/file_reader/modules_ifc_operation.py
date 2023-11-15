# Modules
import os
import ifcopenshell

""" 
New Created Modules
"""

def is_ifc_file(VAR_FILEPATH:str):
    """
    Shall open the IFC-File with the given Filepath, except when it isn't a IFC-File od corrupdet
    
    Parameters:
    - VAR_FILEPATH (str): Filepath
    """
    try:
        # Try to open the IFC file
        ifc_file = ifcopenshell.open(VAR_FILEPATH)
        return True
    except ifcopenshell.exceptions.Error as e:
        # If it's not a IFC file or corrupted it returns False
        return False
    
def extract_file_name(VAR_FILEPATH:str):
    """
    Extracts the Filename and saves it as VAR_FILENAME

    Parameters:
    - VAR_FILEPATH (str): Filepath
    - VAR_FILENAME (str): Filename
    """
    # Extract the base name of the file (excluding the path and extension)
    VAR_FILENAME = os.path.splitext(os.path.basename(VAR_FILEPATH))[0]
    return VAR_FILENAME
