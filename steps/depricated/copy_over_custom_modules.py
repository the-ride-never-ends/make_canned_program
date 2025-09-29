import os
import shutil
import sys

def copy_over_custom_modules(chosen_modules: list, program_path: str) -> None:
    """Copy selected custom modules to the program directory.
    
    Copies each module from the custom_modules directory to the program directory,
    ignoring git files and zone identifier files. Exits on copy errors.
    
    Args:
        chosen_modules (list): List of module names to copy.
        program_path (str): The destination directory for the modules.
        
    Raises:
        SystemExit: If any module copy operation fails.
    """
    custom_modules_path = "../custom_modules"
    for module in chosen_modules:
        src_path = os.path.join(custom_modules_path, module)
        dst_path = os.path.join(program_path, module)
        if os.path.exists(src_path):
            try:
                shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns('.git', '.gitignore','*.Zone-Identifier'))
                print(f"Copied {module} to {dst_path}.")
            except Exception as e:
                print(f"Error: Unable to copy {module} to {dst_path}: {e}")
                sys.exit(1)