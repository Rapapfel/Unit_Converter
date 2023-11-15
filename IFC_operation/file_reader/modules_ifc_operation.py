# Modules
import os
import ifcopenshell
from prettytable import PrettyTable

""" 
New Created Modules
"""
# IFC Path import and validation
def is_ifc_file(VAR_FILEPATH:str):
    """
    Shall open the IFC-File with the given Filepath, except when it isn't a IFC-File od corrupdet
    
    Parameters:
    - VAR_FILEPATH: Filepath
    """
    try:
        # Try to open the IFC file
        ifc_file = ifcopenshell.open(VAR_FILEPATH)
        return True
    except ifcopenshell.exceptions.Error as e:
        # If it's not a IFC file or corrupted it returns False
        return False

# Extract Filename from Filepath
def extract_file_name(VAR_FILEPATH:str):
    """
    Extracts the Filename and saves it as VAR_FILENAME

    Parameters:
    - VAR_FILEPATH: Filepath
    - VAR_FILENAME: Filename
    """
    # Extract the base name of the file (excluding the path and extension)
    VAR_FILENAME = os.path.splitext(os.path.basename(VAR_FILEPATH))[0]
    return VAR_FILENAME

# Create a Unit table that shows all Units
def check_ifc_units(VAR_FILEPATH):
    """
    Checks for the used Unit in the IFC-File

    Parameters:
    - VAR_FILEPATH: Filepath
    """
    try:
        # Open the IFC file
        ifc_file = ifcopenshell.open(VAR_FILEPATH)

        # Create a table for displaying unit information
        table = PrettyTable()
        table.field_names = ["Unit Type", "Name"]

        # Iterate through all IfcUnitAssignment entities
        for unit_assignment in ifc_file.by_type('IfcUnitAssignment'):
            # Iterate through the units in the assignment
            for unit in unit_assignment.Units:
                # Add a row to the table for each unit
                table.add_row([unit.UnitType, unit.Name ])

        # Print the table
        print(table)

    except Exception as e:
        print(f"Error: {e}")

# Check for generall Unit System
def get_general_unit_system(VAR_FILEPATH):
    """
    """
    try:
        # Open the IFC file
        ifc_file = ifcopenshell.open(VAR_FILEPATH)

        # Iterate through all IfcProject entities
        for project in ifc_file.by_type('IfcProject'):
            # Check the unit information in the project
            # !!! NOCH ETWAS FALSCH !!!
            if project.UnitsInContext:
                unit_context = project.UnitsInContext
                if unit_context.LENGTHUNIT:
                    return unit_context.LENGTHUNIT.UnitType

    except Exception as e:
        print(f"Error: {e}")

    # Default to None if unit information is not found
    return None
