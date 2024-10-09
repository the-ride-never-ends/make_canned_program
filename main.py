
import os
import sys


from utils.choose_modules import choose_modules
from utils.create_debug_input_and_output_folders import create_debug_input_and_output_folders
from utils.create_readme import create_readme
from utils.concatenate_requirements import concatenate_requirements
from utils.copy_over_custom_modules import copy_over_custom_modules
from utils.remove_underscores import remove_underscores
from utils.unpack_then_delete import unpack_then_delete
from utils.unpack_utils_shared import unpack_utils_shared


def main():
    """
    Create the base for a program. The program will have the following file structure.
    program_name
    --> main.py
    --> start.bash
    --> install.bash
    --> 
    """
    # Step 1. Name the program
    program_name = input("Enter the name of your program: ")


    # Step 2. Choose custom modules from "custom_modules" folder.
    # NOTE: Always include the folders "main", "start_install_requirements", and ".gitignore"
    always_include = ["main", "start_install", ".gitignore"]
    chosen_modules = choose_modules(always_include)


    # Step 3. Create the folder with chosen program name in the home directory
    home_dir = os.path.expanduser("~")
    program_path = os.path.join(home_dir, program_name)
    if not os.path.exists(program_path):
        os.makedirs(program_path, exist_ok=True)
        print("Made program directory.")
    else:
        print("Error: Program with that name already exists. Exiting...")
        sys.exit(1)


    # Step 4. Copy over the custom modules
    # NOTE: Ignore .git and .gitignore files.
    copy_over_custom_modules(chosen_modules, program_path)


    # Step 5. Concatenate requirements.txt files
    all_requirements = concatenate_requirements(program_path)


    # Step 6. Unpack the "utils.shared" files
    unpack_utils_shared(chosen_modules, program_path)


    # Step 7. Unpack these folders into the program directory, then delete folder
    _unpack_then_delete = ["main", ".gitignore", "start_install"]
    for folder in _unpack_then_delete:
        unpack_then_delete(folder, program_path)


    # Step 8. Create a README.md file.
    create_readme(program_name, program_path, all_requirements)


    # Step 9. Remove the underscore from all file names in the main folder. 
    remove_underscores(program_path)


    # Step 10. Create debug, input, and output folders.
    create_debug_input_and_output_folders()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped.")