import json
import os
from datetime import datetime
import shutil

def create_json_file(template_name, modified_by, description, parameter_data):
    """
    Erstellt eine JSON-Datei mit den angegebenen Daten für ein benutzerdefiniertes Template.

    Args:
    - template_name (str): Der Name des Templates.
    - modified_by (str): Der Benutzer, der das Template zuletzt bearbeitet hat.
    - description (str): Eine Beschreibung des Templates.
    - parameter_data (dict): Ein Dictionary mit den ausgewählten Parametern und deren Einheiten.

    """
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
    """
    Überschreibt eine vorhandene JSON-Datei mit aktualisierten Daten für ein benutzerdefiniertes Template.

    Args:
    - template_name_old (str): Der Name des vorhandenen Templates.
    - template_name_new (str): Der neue Name für das aktualisierte Template.
    - modified_by (str): Der Benutzer, der das Template zuletzt bearbeitet hat.
    - description (str): Eine Beschreibung des Templates.
    - parameter_data (dict): Ein Dictionary mit den ausgewählten Parametern und deren Einheiten.

    """
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
    """
    Entfernt eine JSON-Datei für ein benutzerdefiniertes Template.

    Args:
    - template_name (str): Der Name des zu entfernenden Templates.

    """
    json_filename = os.path.join("Templates/custom_templates", f"{template_name}.json")
    os.remove(json_filename)

def export_json_file(template_name, export_path):
    """
    Exportiert eine JSON-Datei für ein benutzerdefiniertes Template an den angegebenen Exportpfad.

    Args:
    - template_name (str): Der Name des zu exportierenden Templates.
    - export_path (str): Der Dateipfad, unter dem die JSON-Datei exportiert werden soll.

    """
    # Pfad zur JSON-Datei im Verzeichnis "Templates/custom_templates"
    json_filename = os.path.join("Templates/custom_templates", f"{template_name}.json")

    # Laden des JSON-Templates
    with open(json_filename, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    # Exportieren des JSON-Templates in die angegebene Datei
    with open(export_path, 'w', encoding='utf-8') as export_file:
        json.dump(json_data, export_file, ensure_ascii=False, indent=4)

def import_json_file(import_path):
    """
    Importiert eine JSON-Datei von einem angegebenen Importpfad und kopiert sie in das Zielverzeichnis.

    Args:
    - import_path (str): Der Dateipfad, von dem die JSON-Datei importiert werden soll.

    """
    # Bestimmung des Dateinamens aus dem Importpfad
    filename = os.path.basename(import_path)

    # Zielverzeichnis, in das die Datei kopiert werden soll, angepasst an die Struktur der anderen Funktionen
    target_directory = os.path.join("Templates", "custom_templates")
    target_path = os.path.join(target_directory, filename)

    # Kopieren der Datei vom Importpfad zum Zielverzeichnis
    shutil.copy(import_path, target_path)
