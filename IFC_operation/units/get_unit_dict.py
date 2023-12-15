import sympy
from sympy import Symbol, simplify
from sympy.physics import units
from sympy.physics.units.dimensions import Dimension
from itertools import product
import json

def filter_units_by_dimension(unit_dict, dimension):
    return {unit.name for unit in unit_dict.values() if isinstance(unit, units.Unit) and unit.dimension == dimension}

def replace_symbols_in_formula(formula, replacements):
    for symbol, value in replacements.items():
        formula = formula.subs(Symbol(symbol), value)
    return formula

# Sammeln aller verfügbaren Einheiten
all_units = {name: getattr(units, name) for name in dir(units) if isinstance(getattr(units, name), units.Unit)}

# Volumen und Zeit für Volumenstrom auslesen
volume = filter_units_by_dimension(all_units, Dimension("length")**3)
time_units = filter_units_by_dimension(all_units, Dimension("time"))

# Formeln für verschiedene Kategorien
formulas = {
    "Fläche": ["length**2"],
    "Volumen": ["length**3"],
    "Dichte": ["mass / (length**3)"],
    "Volumenstrom": ["(length**3) / time", "volume / time"],
    "Massenstrom": ["mass / time"],
    "Druck": ["force / (length**2)"],
    "Geschwindigkeit": ["length / time"],
    "Beschleunigung": ["length / (time**2)"],
    "Frequenz": ["1 / time"],
    "Ladung": ["current * time"],
    "Spannung": ["(mass * (length**2)) / (current * (time**3))", "energy / charge", "(mass * area) / (current * (time**3))"],
    "Energie": ["force * length", "(mass * (length**2)) / (time**2)", "(mass * area) / (time**2)"],
    "Leistung": ["energy / time", "(mass * (length**2)) / (time**3)", "(mass * area) / (time**3)"],
    "Kraft": ["(mass * length) / (time**2)"]
}

# Funktion zum Erstellen des Units Dictionary
def create_units_dictionary():
    units_dict = {
        "Länge": filter_units_by_dimension(all_units, Dimension('length')),
        "Masse": filter_units_by_dimension(all_units, Dimension('mass')),
        "Zeit": filter_units_by_dimension(all_units, Dimension('time')),
        "Strom": filter_units_by_dimension(all_units, Dimension('current')),
        "Temperatur": filter_units_by_dimension(all_units, Dimension('temperature')),
        "Stoffmenge": filter_units_by_dimension(all_units, Dimension('amount_of_substance')),
        "Lichtstärke": filter_units_by_dimension(all_units, Dimension('luminous_intensity')),
        "Ladung": filter_units_by_dimension(all_units, Dimension('charge')),
        "Spannung": filter_units_by_dimension(all_units, Dimension('voltage')),
        "Digitale Informationen": filter_units_by_dimension(all_units, Dimension('information')),
        "Leistung": filter_units_by_dimension(all_units, Dimension('power')),
        "Energie": filter_units_by_dimension(all_units, Dimension('energy')),
        "Geschwindigkeit": filter_units_by_dimension(all_units, Dimension('velocity')),
        "Beschleunigung": filter_units_by_dimension(all_units, Dimension('acceleration')),
        "Frequenz": filter_units_by_dimension(all_units, Dimension('frequency')),
        "Fläche": filter_units_by_dimension(all_units, Dimension("length")**2),
        "Volumen": filter_units_by_dimension(all_units, Dimension("length")**3),
        "Dichte": filter_units_by_dimension(all_units, Dimension('mass') / (Dimension("length")**3)),
        "Volumenstrom": filter_units_by_dimension(all_units, Dimension("length")**3 / Dimension('time')),
        "Massenstrom": filter_units_by_dimension(all_units, Dimension('mass') / Dimension('time')),
        "Druck": filter_units_by_dimension(all_units, Dimension('pressure')),
        "Kraft": filter_units_by_dimension(all_units, Dimension('force'))
    }

    # Erweitern der Einheiten durch Formeln
    # Erweitern der Einheiten durch Formeln
    for category in units_dict:
        if category in formulas:
            for formula in formulas[category]:
                if 'volume' in formula:
                    # Verwenden Sie die zuvor definierten Volumeneinheiten und iterieren über Zeit-Einheiten
                    for vol_unit in volume:
                        vol_unit_str = str(vol_unit)
                        for time_unit in time_units:
                            time_unit_str = str(time_unit)
                            evaluated_formula = formula.replace('volume', vol_unit_str).replace('time', time_unit_str)
                            evaluated_expr = simplify(evaluated_formula)
                            units_dict[category].add(str(evaluated_expr))
                else:
                    expr = simplify(formula)
                    symbols = expr.free_symbols
                    dimensions_needed = [str(symbol) for symbol in symbols]
                    units_combinations = product(*(filter_units_by_dimension(all_units, Dimension(dim)) for dim in dimensions_needed))

                    for combo in units_combinations:
                        replacements = dict(zip(dimensions_needed, combo))
                        evaluated_formula = replace_symbols_in_formula(expr, replacements)
                        units_dict[category].add(str(evaluated_formula))


    return units_dict

# Erstellen des Dictionaries
units_dictionary = create_units_dictionary()

def convert_symbols_to_strings(obj):
    """
    Rekursive Funktion, um SymPy-Objekte in Strings umzuwandeln
    """
    if isinstance(obj, (Symbol, sympy.Basic)):  # Inkludiert Relational-Objekte
        return str(obj)
    elif isinstance(obj, set):
        return {convert_symbols_to_strings(item) for item in obj}
    elif isinstance(obj, dict):
        return {k: convert_symbols_to_strings(v) for k, v in obj.items()}
    else:
        return obj

def convert_sets_to_lists(obj):
    """
    Rekursive Funktion, um Set-Objekte in sortierte Listen umzuwandeln
    """
    if isinstance(obj, set):
        return sorted([convert_sets_to_lists(item) for item in obj])
    elif isinstance(obj, dict):
        return {k: convert_sets_to_lists(v) for k, v in obj.items()}
    else:
        return obj

# Pfad der Datei, in die das JSON gespeichert werden soll
json_file_path = r'C:\Users\ragre\OneDrive - Hochschule Luzern\DC_Scripting\unit_changer\IFC_operation\units\units.json'

# Erstellen des Dictionaries
units_dictionary = create_units_dictionary()

# Anwenden der Konvertierungsfunktionen
units_dictionary_converted = convert_symbols_to_strings(units_dictionary)
units_dictionary_lists_sorted = convert_sets_to_lists(units_dictionary_converted)

# Schreiben des sortierten JSON-Strings in die Datei
with open(json_file_path, 'w') as file:
    json.dump(units_dictionary_lists_sorted, file, indent=4)