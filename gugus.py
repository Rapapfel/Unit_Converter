import ifcopenshell

# Öffnen der IFC-Datei
ifc_file = ifcopenshell.open("C:/Users/ragre/OneDrive - Hochschule Luzern/DC_Scripting/Beispiel_IFC/Claridenstrasse 25, 8002 Zürich - Kopie.ifc")

# Zählen der Komponenten
komponenten = {}

for entity in ifc_file.by_type('IfcProduct'):
    entity_name = entity.is_a()
    if entity_name in komponenten:
        komponenten[entity_name] += 1
    else:
        komponenten[entity_name] = 1

# Ausgabe der Anzahl der Komponenten
for komponente, anzahl in komponenten.items():
    print(f"{komponente}: {anzahl}")
