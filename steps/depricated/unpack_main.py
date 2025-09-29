
import os
import shutil

    # Step 7. Unpack the main folder into the program directory, then delete the main folder
def unpack_main(program_path: str) -> None:
    """Unpack the main folder contents into the program directory.
    
    Moves all contents from the 'main' subfolder to the root program directory,
    renaming '_main.py' to 'main.py' in the process. Removes the main folder
    after unpacking.
    
    Args:
        program_path (str): The path to the program directory containing the main folder.
    """
    main_folder = os.path.join(program_path, "main")
    if os.path.exists(main_folder):
        for item in os.listdir(main_folder):
            s = os.path.join(main_folder, item)
            d = os.path.join(program_path, item)
            if item == "_main.py":
                shutil.move(s, os.path.join(program_path, "main.py"))
                print("Renamed _main.py to main.py and moved to program directory")
            elif os.path.isdir(s):
                shutil.copytree(s, d, ignore=shutil.ignore_patterns('.git', '.gitignore'))
                print(f"Copied directory {item} to program directory")
            else:
                shutil.copy2(s, d)
                print(f"Copied file {item} to program directory")
        shutil.rmtree(main_folder)
        print("Removed main folder")
