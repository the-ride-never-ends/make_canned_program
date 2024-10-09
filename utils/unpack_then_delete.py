import os
import shutil

def unpack_then_delete(folder_name: str, program_path: str) -> None:
    folder_path = os.path.join(program_path, folder_name)
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            s = os.path.join(folder_path, item)
            d = os.path.join(program_path, item)
            if os.path.exists(d):
                print(f"{item} already exists in the program directory. Skipping...")
                continue

            if os.path.isdir(s):
                shutil.copytree(s, d, ignore=shutil.ignore_patterns('.git', '.gitignore'))
                print(f"Copied directory {item} to program directory")
            else:
                shutil.copy2(s, d)
                print(f"Copied file {item} to program directory")

        shutil.rmtree(folder_path)
        print(f"Removed {folder_name} folder")

