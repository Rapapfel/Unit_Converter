import os
import ifcopenshell
from sympy import symbols, sympify
from sympy.physics.units import convert_to
import sympy.physics.units as u
import json
from tqdm import tqdm

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

# Funktion zum Parsen der Einheiten
def parse_unit(unit_str):
    # Ersetzt Multiplikations- und Divisionssymbole für das Parsing
    unit_str = unit_str.replace('/', ' / ').replace('*', ' * ')
    # Erstellt einen sympy-Ausdruck aus dem String
    return sympify(unit_str, locals=u.__dict__)

# Extract, Convert and Resave Units
def convert_value(value, source_unit_str, target_unit_str, decimal_places=2):
    x = symbols('x')
    source_unit = parse_unit(source_unit_str)
    target_unit = parse_unit(target_unit_str)
    converted_expr = convert_to(value * source_unit, target_unit).subs(x, 1)
    # Extrahiert den numerischen Wert
    converted_value = converted_expr.evalf()
    # Trennt den numerischen Wert von der Einheit
    numeric_value = converted_value.as_coeff_Mul()[0]
    # Rundet auf die gewünschte Anzahl von Dezimalstellen
    rounded_value = round(float(numeric_value), decimal_places)
    return rounded_value

def extract_data_and_update_ifc(VAR_FILEPATH, selected_save_file_path, template_name):

    """
    Imports from the IFC-File (VAR_FILEPATH) all selected Psets (dict_selected_type) with the selected properties (dict_selected_properties).
    Then converts eache of the selected properties with the already selected units to the also selected target unit.
    
    Parameters:
    - VAR_FILEPATH: Filepath
    - dict_selected_type: The Dictionary with the selected Pset's
    - dict_selected_properties: The Dictionary with the selectedfilepath
    """

    # Pfad des aktuellen Skripts und Pfad zum JSON-File
    current_script = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(current_script, "..", "..", "Templates", "custom_templates",template_name+".json")

    # Laden des JSON-Files
    with open(json_path, "r") as file:
        template_data = json.load(file)

    # Extraktion der 'parameters' aus dem JSON-File
    selected_dict = template_data.get("parameters", {})

    # Load the IFC file
    ifc_file = ifcopenshell.open(VAR_FILEPATH)
    ID_set= set()

    for dict_packet in selected_dict.keys():
        key_list = dict_packet.split(" â€” ")

        # Iterate through all IfcPropertySet objects in the IFC file
        for ifc_pset in tqdm(ifc_file.by_type("IfcPropertySet")):
            pset_name = ifc_pset.Name
            # Check if the current PSet is in the selected parameters
            if pset_name in key_list[0]:
                # Iterate through the properties within the PSet
                for ifc_property in ifc_pset.HasProperties:
                    ID = str(ifc_property).split("=")[0]
                    if ID in ID_set:
                        continue
                    else:
                        ID_set.add(ID)

                    # Extract category name from the property
                    property_category = ifc_property.Name

                    # Check if the category is in the selected parameters
                    if property_category == key_list[1]:
                        source_unit_name = selected_dict[dict_packet]['source_unit']
                        target_unit_name = selected_dict[dict_packet]['target_unit']
                        # print (property_category,source_unit_name, target_unit_name)

                        # Access and convert property value using sympy
                        property_value = getattr(ifc_property, "NominalValue", None).wrappedValue
                        # print(property_value)

                        if property_value is not None:
                            converted_value = convert_value(property_value, source_unit_name, target_unit_name)
                            # print("Converted-Value", converted_value)

                            # Update the IFC file with the converted value
                            ifc_property.NominalValue.wrappedValue = converted_value


    # Save the modified IFC file
    ifc_file.write(selected_save_file_path)





