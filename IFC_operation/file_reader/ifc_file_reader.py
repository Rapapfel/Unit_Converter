# External Modules


# Internal Modules

import modules_ifc_operation as modules

# Used Variables
VAR_FILENAME = None
unit_system = None



# Import File and validation
# As long as a Error occurs, input phase stays active
file_imported = False
while file_imported == False:

    VAR_FILEPATH = input("User input:\tPlease enter the Filepath:\t")

    # Validate Import
    if modules.is_ifc_file(VAR_FILEPATH) == True:
        file_imported = True
        print("System Message:\tFile imported")
    else:
        file_imported = False
        print("System Message:\tError Message")

# Extract Filename
VAR_FILENAME = modules.extract_file_name(VAR_FILEPATH)
print("System Message:\t"+VAR_FILENAME)

# Check for Unit
wannasee = input("System Message:\tDo you want to see the Unit table? y/n\n")
if wannasee == "y":
    modules.check_ifc_units(VAR_FILEPATH)

unit_system = modules.get_general_unit_system(VAR_FILEPATH)
if unit_system:
    print(f"System MEssage:\tThe general unit system of the IFC file is: {unit_system}")
else:
    print("System Message:\tUnable to determine the general unit system.")
    modules.check_ifc_units(VAR_FILEPATH)
    unit_system = input("User input:\tChoose between SI, Imperial, Metric, Custom based on the table\t")
