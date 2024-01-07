from sympy import symbols, sympify
from sympy.physics.units import convert_to
import sympy.physics.units as u

# Funktion zum Parsen der Einheiten
def parse_unit(unit_str):
    """
    Diese Funktion analysiert und parst eine Zeichenkette, die eine Einheit darstellt.

    Args:
    - unit_str (str): Die Zeichenkette, die die Einheit darstellt.

    Returns:
    - Ein sympy-Ausdruck, der die geparste Einheit repräsentiert.
    """
    # Ersetzt Multiplikations- und Divisionssymbole für das Parsing
    unit_str = unit_str.replace('/', ' / ').replace('*', ' * ')
    # Erstellt einen sympy-Ausdruck aus dem String
    return sympify(unit_str, locals=u.__dict__)

# Funktion zur Einheitenkonvertierung
def convert_value(value, source_unit_str, target_unit_str, decimal_places=5):
    """
    Diese Funktion führt eine Einheitenkonvertierung für einen gegebenen Wert von einer Quelleinheit in eine Zieleinheit durch.

    Args:
    - value (float): Der zu konvertierende Wert.
    - source_unit_str (str): Die Quelleinheit, z.B. 'meter**3/hour'.
    - target_unit_str (str): Die Zieleinheit, z.B. 'meter**3/second'.
    - decimal_places (int): Die Anzahl der Dezimalstellen im konvertierten Wert (Standardwert ist 5).

    Returns:
    - Der konvertierte Wert als float.
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
    rounded_value = round(numeric_value, decimal_places)
    return rounded_value

if __name__ == "__main__":
    # Beispiel für die Verwendung
    value = float(3600.5)  # Beispielswert
    source_unit = 'meter**3/hour'  # Quelleinheit
    target_unit = 'meter**3/second'  # Zieleinheit

    # Konvertierung durchführen
    converted_value = convert_value(value, source_unit, target_unit)

    # Ergebnis anzeigen
    print(f"Konvertierter Wert: {converted_value}")
