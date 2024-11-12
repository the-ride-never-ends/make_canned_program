import os
import shutil
import sys

def copy_over_custom_modules(chosen_modules: list, program_path: str) -> None:
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