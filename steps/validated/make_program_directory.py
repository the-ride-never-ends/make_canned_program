import os
import sys

def make_program_directory(program_name: str, preferred_path: str = None) -> str:
    """Create a new program directory with the given name.
    
    Creates a directory for the program in either the user's home directory
    or a specified preferred path. Exits if a directory with the same name
    already exists.
    
    Args:
        program_name (str): The name of the program directory to create.
        preferred_path (str, optional): The preferred base path for the directory.
            If None, uses the user's home directory. Defaults to None.
            
    Returns:
        str: The absolute path of the created program directory.
        
    Raises:
        SystemExit: If a directory with the program name already exists.
    """
    home_dir = os.path.expanduser("~")
    program_path = os.path.join(home_dir, program_name) if not preferred_path else os.path.join(preferred_path, program_name)
    if not os.path.exists(program_path):
        os.makedirs(program_path, exist_ok=True)
        print(f"Made program directory at {program_path}")
        return program_path
    else:
        print("Error: Program with that name already exists. Exiting...")
        sys.exit(1)
