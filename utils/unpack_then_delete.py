import os
import shutil


def unpack_then_delete(these_files: list[str], program_path: str) -> None:
    """
    Unpacks contents from specified folders to the program directory and then deletes the source folders.
    It skips items that already exist in the destination, as well as .git and .gitignore files/directories.

    Args:
        these_files (list[str]): A list of folder names to process.
        program_path (str): The path to the program directory where contents will be copied.
    """
    ignore = shutil.ignore_patterns('.git', '.gitignore')
    program_name = os.path.basename(program_path)

    _unpack_then_delete = [
        os.path.join(program_path, folder) 
        for folder in these_files 
        if os.path.exists(os.path.join(program_path, folder))
    ]

    for path in _unpack_then_delete:
        for item in os.listdir(path):
            source_path = os.path.join(path, item)
            destination_path = os.path.join(program_path, item)

            # Skip if the item already exists in the program directory
            if os.path.exists(destination_path):
                print(f"{item} already exists in the program directory. Skipping...")
                continue

            # Copy over the file or directory
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path, ignore=ignore)
                print(f"Copied directory {item} to {program_name}")
            else:
                shutil.copy2(source_path, destination_path)
                print(f"Copied file {item} to {program_name}")

        # Remove the source folder once everything is copied.
        shutil.rmtree(path)
        print(f"Removed {os.path.basename(path)} folder")
