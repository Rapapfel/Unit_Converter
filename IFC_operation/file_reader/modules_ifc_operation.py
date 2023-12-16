# Modules
import os
import ifcopenshell # Python 3.11!
from prettytable import PrettyTable
from sympy.physics.units import *

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
    except Exception as e:
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

# alle IFC Parameter in Dictionary
def extract_pset_parameters(VAR_FILEPATH):
    try:
        ifc_file = ifcopenshell.open(VAR_FILEPATH)
        pset_dict = {}

        # Durchlaufen aller Elemente, die Eigenschaften haben könnten
        for element in ifc_file.by_type("IfcElement"):
            # Durchlaufen aller Definitionen, die einem Element zugeordnet sind
            for definition in element.IsDefinedBy:
                if definition.is_a("IfcRelDefinesByProperties"):
                    pset = definition.RelatingPropertyDefinition
                    if pset.is_a("IfcPropertySet"):
                        pset_name = pset.Name
                        property_names = [prop.Name for prop in pset.HasProperties]
                        # Hinzufügen oder Aktualisieren des Pset-Namens im Dictionary
                        if pset_name not in pset_dict:
                            pset_dict[pset_name] = property_names
                        else:
                            # Doppelte Eigenschaftsnamen vermeiden
                            pset_dict[pset_name].extend(x for x in property_names if x not in pset_dict[pset_name])
                    elif pset.is_a("IfcElementQuantity"):
                        # Ähnliche Logik kann für IfcElementQuantity und andere Arten von Eigenschaftsdefinitionen angewendet werden
                        pass

        # Entfernen von Duplikaten und Sortieren der Eigenschaftsnamen in jeder Pset-Liste
        for pset_name in pset_dict:
            pset_dict[pset_name] = sorted(set(pset_dict[pset_name]))

        return pset_dict

    except Exception as e:
        print(f"Fehler beim Extrahieren von Pset-Parametern: {e}")
        return {}

# Extract, Convert and Resave Units
def convert_value(value, source_unit_name, target_unit_name):
    # Convert the value using sympy's convert_to function
    converted_value = convert_to(value * source_unit_name, target_unit_name).evalf().args[0]
    return converted_value

def extract_data_and_update_ifc(ifc_file_path, selected_parameters):
    """
    Imports from the IFC-File (VAR_FILEPATH) all selected Psets (dict_selected_type) with the selected properties (dict_selected_properties).
    Then converts eache of the selected properties with the already selected units to the also selected target unit.
    
    Parameters:
    - VAR_FILEPATH: Filepath
    - dict_selected_type: The Dictionary with the selected Pset's
    - dict_selected_properties: The Dictionary with the selected
    """
    # Load the IFC file
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Iterate through all IfcPropertySet objects in the IFC file
    for ifc_pset in ifc_file.by_type("IfcPropertySet"):
        pset_name = ifc_pset.Name

        # Check if the current PSet is in the selected parameters
        if pset_name in selected_parameters:
            print(f"Processing PSet: {pset_name}")

            # Iterate through the properties within the PSet
            for ifc_property in ifc_pset.HasProperties:
                # Extract category name from the property
                property_category = getattr(ifc_property, "CategoryName", None)

                # Check if the category is in the selected parameters
                if property_category in selected_parameters[pset_name]:
                    category_info = selected_parameters[pset_name][property_category]
                    source_unit_name = category_info['source_unit']
                    target_unit_name = category_info['target_unit']

                    # Access and convert property value using sympy
                    property_value = getattr(ifc_property, "NominalValue", None)

                    if property_value is not None:
                        converted_value = convert_value(property_value, source_unit_name, target_unit_name)

                        # Update the IFC file with the converted value
                        setattr(ifc_property, "NominalValue", converted_value)

                        # Print or log the extracted and converted information
                        print(f"  Category: {property_category}")
                        print(f"  Property: {ifc_property.Name}")
                        print(f"  Source Unit: {source_unit_name}, Target Unit: {target_unit_name}")
                        print(f"  Original Value: {property_value}")
                        print(f"  Converted Value: {converted_value}")
                        print("------------------------")

    # Save the modified IFC file
    ifc_file.write(ifc_file_path)



