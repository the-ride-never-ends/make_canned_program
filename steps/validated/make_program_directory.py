import os
import sys

def make_program_directory(program_name: str, preferred_path: str = None) -> str:
    home_dir = os.path.expanduser("~")
    program_path = os.path.join(home_dir, program_name) if not preferred_path else os.path.join(preferred_path, program_name)
    if not os.path.exists(program_path):
        os.makedirs(program_path, exist_ok=True)
        print(f"Made program directory at {program_path}")
        return program_path
    else:
        print("Error: Program with that name already exists. Exiting...")
        sys.exit(1)
