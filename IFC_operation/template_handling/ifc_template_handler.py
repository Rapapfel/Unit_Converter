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

    # Korrigierter Pfad unter Verwendung von Raw String (r)
    json_filename = os.path.join(r"C:\Users\ragre\OneDrive - Hochschule Luzern\DC_Scripting\unit_changer\Templates\custom templates", f"{template_name}.json")
    
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

# Beispielaufruf der Funktion
if __name__ == "__main__":
    template_name = "Monoblock Parameter7"
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
