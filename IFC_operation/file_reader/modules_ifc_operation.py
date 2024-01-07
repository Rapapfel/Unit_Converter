import os
import ifcopenshell
from sympy import symbols, sympify
from sympy.physics.units import convert_to
import sympy.physics.units as u
import json
from tqdm import tqdm

# IFC-Pfad importieren und validieren
def is_ifc_file(VAR_FILEPATH:str):
    """
    Diese Funktion versucht, die IFC-Datei mit dem angegebenen Dateipfad zu öffnen, es sei denn, es handelt sich nicht um eine IFC-Datei oder sie ist beschädigt.

    Args:
    - VAR_FILEPATH (str): Dateipfad zur IFC-Datei.

    Returns:
    - bool: True, wenn die Datei eine gültige IFC-Datei ist, andernfalls False.
    """
    try:
        # Versuchen, die IFC-Datei zu öffnen
        ifc_file = ifcopenshell.open(VAR_FILEPATH)
        return True
    except Exception as e:
        # Wenn es sich nicht um eine IFC-Datei handelt oder sie beschädigt ist, wird False zurückgegeben
        return False

# Alle IFC-Parameter in ein Dictionary extrahieren
def extract_pset_parameters(VAR_FILEPATH):
    """
    Diese Funktion extrahiert alle Pset-Parameter aus einer IFC-Datei und gibt sie in Form eines Dictionaries zurück.

    Args:
    - VAR_FILEPATH (str): Dateipfad zur IFC-Datei.

    Returns:
    - dict: Ein Dictionary, das Pset-Namen als Schlüssel und Listen von Parameter-Namen als Werte enthält.
    """
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
    """
    Diese Funktion ersetzt Multiplikations- und Divisionssymbole im Einheitenstring und erstellt einen sympy-Ausdruck daraus.

    Args:
    - unit_str (str): Einheitenstring.

    Returns:
    - sympy.Expr: Ein sympy-Ausdruck, der die Einheiten repräsentiert.
    """
    # Ersetzt Multiplikations- und Divisionssymbole für das Parsen
    unit_str = unit_str.replace('/', ' / ').replace('*', ' * ')
    # Erstellt einen sympy-Ausdruck aus dem String
    return sympify(unit_str, locals=u.__dict__)

# Funktion zum Konvertieren von Werten zwischen Einheiten
def convert_value(value, source_unit_str, target_unit_str, decimal_places=2):
    """
    Konvertiert einen Wert von einer Quelleinheit in eine Zieleinheit und rundet das Ergebnis auf die gewünschte Anzahl von Dezimalstellen.

    Args:
    - value (float): Der zu konvertierende Wert.
    - source_unit_str (str): Einheitenstring der Quelleinheit.
    - target_unit_str (str): Einheitenstring der Zieleinheit.
    - decimal_places (int, optional): Anzahl der Dezimalstellen für das gerundete Ergebnis. Standardmäßig auf 2 gesetzt.

    Returns:
    - float: Der konvertierte und gerundete Wert.
    """
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
    Extrahiert aus der IFC-Datei (VAR_FILEPATH) alle ausgewählten Psets (dict_selected_type) mit den ausgewählten Eigenschaften (dict_selected_properties).
    Konvertiert dann jede der ausgewählten Eigenschaften mit den bereits ausgewählten Einheiten in die ebenfalls ausgewählte Ziel-Einheit.

    Args:
    - VAR_FILEPATH (str): Dateipfad zur IFC-Datei.
    - selected_save_file_path (str): Dateipfad, unter dem die aktualisierte IFC-Datei gespeichert wird.
    - template_name (str): Der Name des Templates.

    """
    # Pfad des aktuellen Skripts und Pfad zum JSON-File
    current_script = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(current_script, "..", "..", "Templates", "custom_templates",template_name+".json")

    # Laden des JSON-Files
    with open(json_path, "r") as file:
        template_data = json.load(file)

    # Extraktion der 'parameters' aus dem JSON-File
    selected_dict = template_data.get("parameters", {})

    # Laden der IFC-Datei
    ifc_file = ifcopenshell.open(VAR_FILEPATH)
    ID_set= set()

    for dict_packet in selected_dict.keys():
        key_list = dict_packet.split(" — ")

        # Durchlaufen aller IfcPropertySet-Objekte in der IFC-Datei
        for ifc_pset in tqdm(ifc_file.by_type("IfcPropertySet")):
            pset_name = ifc_pset.Name
            # Überprüfen, ob das aktuelle PSet in den ausgewählten Parametern ist
            if pset_name in key_list[0]:
                # Durchlaufen der Eigenschaften innerhalb des PSet
                for ifc_property in ifc_pset.HasProperties:
                    ID = str(ifc_property).split("=")[0]
                    if ID in ID_set:
                        continue
                    else:
                        ID_set.add(ID)

                    # Extrahieren des Kategorienamen aus der Eigenschaft
                    property_category = ifc_property.Name

                    # Überprüfen, ob die Kategorie in den ausgewählten Parametern ist
                    if property_category == key_list[1]:
                        source_unit_name = selected_dict[dict_packet]['source_unit']
                        target_unit_name = selected_dict[dict_packet]['target_unit']

                        # Zugriff und Konvertierung des Eigenschaftswerts unter Verwendung von sympy
                        property_value = getattr(ifc_property, "NominalValue", None).wrappedValue

                        if property_value is not None:
                            converted_value = convert_value(property_value, source_unit_name, target_unit_name)

                            # Aktualisieren der IFC-Datei mit dem konvertierten Wert
                            ifc_property.NominalValue.wrappedValue = converted_value

    # Speichern der modifizierten IFC-Datei
    ifc_file.write(selected_save_file_path)
