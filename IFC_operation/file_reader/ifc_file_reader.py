# External Modules


# Internal Modules
import modules_ifc_operation as modules

# Used Variables
VAR_FILEPATH = None
VAR_FILENAME = None

# Import File and validation
# As long as a Error occurs, input phase stays active
while file_imported == False:
    VAR_FILEPATH = input("Please enter the Filepath")

    # Validate Import
    if modules.is_ifc_file(VAR_FILEPATH) == True:
        file_imported = True
        print("File imported")
    else:
        file_imported = False
        print("Error Message")

# Extract Filename
VAR_FILENAME = modules.extract_file_name(VAR_FILEPATH)
