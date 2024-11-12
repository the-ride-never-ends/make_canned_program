
import os
import sys


from steps.validated.choose_modules import ChooseModule
from steps.validated.copy_on_disk_modules_to_program_directory import CopyOnDiskModulesToProgramDirectory
from steps.validated.make_program_directory import make_program_directory
from steps.validated.concatenate_requirements import concatenate_requirements

from steps.wip.pull_remote_modules_from_github import PullRemoteModulesFromGithub


from utils.create_debug_input_and_output_folders import create_debug_input_and_output_folders
from utils.create_readme import create_readme

from utils.remove_underscores import remove_underscores
from utils.unpack_then_delete import unpack_then_delete
from utils.unpack_utils_shared import unpack_utils_shared
from utils.shared.next_step import next_step


from config.config import OUTPUT_FOLDER
from logger.logger import Logger
logger = Logger(logger_name=__name__)


def main():
    """
    Create the base for a program. The program will have the following file structure.
    program_name/
    ├── main.py
    ├── start.bash
    ├── install.bash
    ├── config/
    │   └── config.py
    ├── logger/
    │   └── logger.py
    ├── debug_logs/
    ├── input/
    ├── output/
    ├── utils/
    |   └── shared/
    ...
    """

    next_step("Step 1. Name the program")
    program_name = input("Enter the name of your program: ")


    next_step("Step 2. Choose custom modules to include in your program.")
    always_include = ["main", "start", "install",
                      "gitignore", "requirements", "readme",
                      "logger", "config", "utils"]
    choose = ChooseModule(always_include=always_include)
    chosen_modules = choose.modules()


    next_step("Step 3. Create the folder with chosen program name in the home directory.")
    program_path = make_program_directory(program_name, preferred_path=OUTPUT_FOLDER)


    next_step("Step 4. Copy the on-disk modules to the program directory.")
    # NOTE: Ignore .git and .gitignore files.
    copy = CopyOnDiskModulesToProgramDirectory(chosen_modules, program_path)
    copy.modules_to_program_directory()


    # TODO This function works as intended, but throws [WinError 5] Access is denied.
    next_step("Step 5. Pull the requested modules from GitHub or disk.")
    pull = PullRemoteModulesFromGithub(chosen_modules, program_path)
    pull.remote_modules_from_github()


    next_step("Step 6. Concatenate requirements.txt files.")
    all_requirements = concatenate_requirements(program_path)


    next_step("Step 7. Unpack the 'utils.shared' files.", stop=True)
    unpack_utils_shared(chosen_modules, program_path)


    these_files = ["main", "gitignore", "start", "install"]
    next_step("Step 8. Unpack these folders into the program directory, then delete the folders")
    unpack_then_delete(these_files, program_path)


    next_step("Step 9. Create a README.md file.")
    create_readme(program_name, program_path, all_requirements)


    next_step("Step 10. Remove underscores from all file names in the main folder.")
    remove_underscores(program_path)


    next_step("Step 11. Create debug, input, and output folders.")
    create_debug_input_and_output_folders(program_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped.")