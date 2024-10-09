
import os

def remove_underscores(program_path: str):
    """
    Remove leading underscore from all files.
    - Change "_gitignore" to ".gitignore"
    """
    for file in os.listdir(program_path):
        if file.startswith("_"):
            old_path = os.path.join(program_path, file)
            if file == "_gitignore":
                new_file = ".gitignore"
            else:
                new_file = file[1:]  # Remove the leading underscore
            new_path = os.path.join(program_path, new_file)
            try:
                os.rename(old_path, new_path)
            except Exception as e:
                print(f"Exception in remove_underscores: {e}")
            print(f"Renamed '{old_path}' to '{new_path}'")

