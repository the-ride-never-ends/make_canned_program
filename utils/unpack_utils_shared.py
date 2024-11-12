import os
import shutil
from pathlib import Path


from logger.logger import Logger
logger = Logger(logger_name=__name__)

from utils.remove_readonly import remove_readonly

def unpack_utils_shared(chosen_modules: list, program_path: str) -> None:
    """
    Unpacks and consolidates the 'utils/shared' directories from multiple modules into a single main 'utils/shared' directory.
    
    This function performs the following tasks:
    1. Identifies 'utils/shared' directories in the chosen modules.
    2. Creates a main 'utils/shared' directory if it doesn't exist.
    3. Copies files and directories from each module's 'utils/shared' to the main 'utils/shared',
       avoiding overwriting existing files.
    4. Removes the individual 'utils/shared' directories from each module after consolidation.

    Args:
        chosen_modules (list): A list of module names to process.
        program_path (str): The base path of the program where modules and the main 'utils/shared' are located.

    Returns:
        None

    Note:
        - This function uses shutil to copy files and directories.
        - It ignores '.git' and '.gitignore' files/directories during the copy process.
    """
    logger.debug("Starting function...")
    ignore = shutil.ignore_patterns('.git', '.gitignore')

    for module in chosen_modules:
        full_path = os.path.join(program_path, module, "utils", "shared")
        logger.debug(f"Checking path: {full_path}")
        logger.debug(f"Path exists: {os.path.exists(full_path)}")

    # Define the destination and source paths for utils.shared
    destination_path = os.path.join(program_path, "utils", "shared")
    utils_shared_sources = {
        module: os.path.join(program_path, module, "utils", "shared")
        for module in chosen_modules
        if os.path.exists(os.path.join(program_path, module, "utils", "shared"))
    }
    if not utils_shared_sources:
        logger.info("No utils.shared directories found in chosen modules. Skipping...")
        return

    for module, path in utils_shared_sources.items():
        logger.info(f"Unpacking utils.shared from {module}...")
        if os.path.exists(path):
            # Copy over the files from the module's utils.shared to the main utils.shared
            # if main utils.shared doesn't exist yet or if the file doesn't exist in main utils.shared.
            if not os.path.exists(destination_path):
                shutil.copytree(path, destination_path, ignore=ignore)
                logger.info(f"Unpacked utils.shared for {module}")

            else:
                # Get all the files and directories in the module's utils.shared
                for item in Path(utils_shared_sources).glob('**/*'):
                    relative_path = item.relative_to(utils_shared_sources)
                    destination_item = Path(destination_path) / relative_path

                    if not destination_item.exists():
                        if item.is_dir(): # Copy the directory and its contents
                            shutil.copytree(item, destination_item, ignore=ignore)
                        else: # Copy the file.
                            shutil.copy2(item, destination_item)
                        logger.info(f"Copied {relative_path} from {module}'s utils.shared to main utils.shared")
                    else: # Don't overwrite files if they're already there.
                        logger.info(f"Skipped {relative_path} from {module}'s utils.shared, as it already exists in main utils.shared")

        # Remove each individual module's utils.shared folder
        # TODO This is what is throwing the error. Need to figure out why.
        if os.path.exists(path):
            shutil.rmtree(path, onexc=remove_readonly)
            print(f"Removed {module}'s utils.shared folder")

        logger.info(f"Finished processing {module}'s utils.shared folder.")
    logger.info(f"All utils.shared unpacked. Ending unpack_utils_shared function.")