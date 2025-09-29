import os

def create_readme(program_name: str, program_path: str, all_requirements: set):
    """Create a README.md file for the program with basic template structure.
    
    Args:
        program_name (str): The name of the program to be used as the title.
        program_path (str): The directory path where the README.md file will be created.
        all_requirements (set): A set of dependency names to be listed in the README.
    """
    dependencies = "\n- ".join(list(all_requirements))
    readme_file_cont = f"# {program_name}\n\n## Overview\n\n## Key Features\n\n## Dependencies\n- {dependencies}\n\n## Usage"

    with open(os.path.join(program_path, "README.md"), 'w') as f:
        f.write(readme_file_cont)

    print("Made README.md for main program")
    print(f"\nProgram '{program_name}' has been created successfully in {program_path}.")
