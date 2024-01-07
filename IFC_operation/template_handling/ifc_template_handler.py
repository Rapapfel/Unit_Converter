import json
import os
from datetime import datetime

def create_json_file(template_name, modified_by, description, parameter_data):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    json_data = {
        "template_name": template_name,
        "last_modified": current_time,
        "modified_by": modified_by,
        "description": description,
        "parameters": parameter_data
    }

    # Relativer Pfad zur JSON-Datei im Verzeichnis "Templates/custom_templates"
    json_filename = os.path.join("Templates/custom_templates", f"{template_name}.json")
    
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)



def overwrite_json_file(template_name_old, template_name_new, modified_by, description, parameter_data):
    # Bestimmung des Pfads der existierenden JSON-Datei
    json_filename_old = os.path.join("Templates/custom_templates", f"{template_name_old}.json")

    os.remove(json_filename_old)

    # Aktuelles Datum und Uhrzeit für die letzte Änderung
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Erstellung der neuen JSON-Daten
    json_data_new = {
        "template_name": template_name_new,
        "last_modified": current_time,
        "modified_by": modified_by,
        "description": description,
        "parameters": parameter_data
    }

    # Pfad für die neue JSON-Datei
    json_filename_new = os.path.join("Templates/custom_templates", f"{template_name_new}.json")

    # Schreiben der neuen Daten in die Datei
    with open(json_filename_new, 'w', encoding='utf-8') as json_file:
        json.dump(json_data_new, json_file, ensure_ascii=False, indent=4)

def remove_json_file(template_name):
    json_filename = os.path.join("Templates/custom_templates", f"{template_name}.json")
    os.remove(json_filename)

# Beispielaufruf der Funktion
if __name__ == "__main__":
    template_name = "Monoblock Paramet20"
    modified_by = "GREA"
    description = "Vorlage mit verschiedenen Parametern für Monoblock-Geräte in der Kältetechnik."
    parameters = {
        "Kälteleistung": {
            "source_unit": "kW",
            "target_unit": "BTU/h"
        },
        "Energieverbrauch": {
            "source_unit": "kWh",
            "target_unit": "J"
        },
        "Schallleistungspegel": {
            "source_unit": "dB",
            "target_unit": "dB(A)"
        },
        "Kältemittelmenge": {
            "source_unit": "kg",
            "target_unit": "lb"
        },
        "Abmessungen": {
            "source_unit": "mm",
            "target_unit": "inch"
        }
    }

    create_json_file(template_name, modified_by, description, parameters)
