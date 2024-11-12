import os
from pathlib import Path
from typing import Optional
import yaml


from config.config import CUSTOM_MODULES_FOLDER, PROJECT_ROOT
from logger.logger import Logger
logger = Logger(logger_name=__name__)


# class ChooseModule:

#     YAML_PATH: str = os.path.join(PROJECT_ROOT, "github_urls_for_modules.yaml")

#     def __init__(self, always_include: list[str] = None) -> None:
        
#         self.github_urls: dict = {
#             "_default": "_option"
#         }
#         # Open the YAML file with the github urls in it and assign it.
#         with open(self.YAML_PATH, "r") as f:
#             try:
#                 self.github_urls: dict = yaml.safe_load(f)
#             except Exception as e:
#                 logger.warning(f"Could not import URL yaml file: {e}\nDefaulting to all on disk options...")

#         self.always_include: list[str] = [module.lower() for module in always_include] or []
#         self.modules_available_on_github: dict = self._get_modules_that_are_available_on_github()
#         self.modules_available_on_disk: dict = self._get_modules_that_are_available_on_disk(CUSTOM_MODULES_FOLDER)

#         # Default to including every single module we have access to.
#         self.available_modules: dict = {**self.modules_available_on_disk, **self.modules_available_on_github}


#     def _load_github_urls(self) -> dict[str, str]:
#         """Load and validate GitHub URLs from YAML file."""
#         try:
#             with open(self.YAML_PATH) as f:
#                 urls = yaml.safe_load(f)
#                 urls = dict(urls)  # Ensure it's a dictionary
            
#             if not isinstance(urls, dict):
#                 raise ValueError("YAML file must contain a dictionary")
            
#             return urls
#         except Exception as e:
#             logger.warning(f"Could not import URL yaml file: {e}")
#             return {"_default": "_option"}


#     def _get_modules_that_are_available_on_github(self) -> dict[str, str]:
#         """
#         Create a dictionary of modules that are available on github.
#         """
#         _available_modules = {
#             module_name: url for module_name, url in self.github_urls.items()
#         }
#         logger.debug(f"_available_modules\n{_available_modules}")

#         return _available_modules


#     def _get_modules_that_are_available_on_disk(self, base_path) -> dict[str, str]:
#         """
#         Get all subfolders one level down from the given base path.
        
#         Args:
#             base_path (str): The base directory path to search in
            
#         Returns:
#             list: dictionary of subfolder paths
#         """
#         # Get the module folders
#         subfolders = {
#             os.path.basename(d): os.path.join(base_path, d)
#                 for d in os.listdir(base_path)
#                 if os.path.isdir(os.path.join(base_path, d))
#                 and os.path.basename(d) not in self.modules_available_on_github # Prefer github over on disk modules
#         }

#         # Get rid of the bash folder if we're on Windows, else get rid of the batch folder.
#         if os.name == 'nt':
#             subfolders.pop('bash', None)
#         else:
#             subfolders.pop('batch', None)
#         logger.debug(f"subfolders\n{subfolders}")

#         return subfolders


#     def choose_modules(self) -> dict[str,str]:
#         """
#         Chose which modules we want to pull from Github or disk.
#         """
#         logger.debug(f"available_modules: {self.available_modules}")

#         # Convert all keys to lowercase for case-insensitive comparison
#         self.available_modules = {k.lower(): v for k, v in self.available_modules.items()}

#         # Print the available modules, excluding the ones that we're always including.
#         available_list = "\n".join(
#             f"- {folder}" for folder in sorted(self.available_modules.keys())
#             if folder not in self.always_include
#         )
#         separator = "*" * 20

#         # Present the available module options to the user and get their choice.
#         print(f"{separator}\nAvailable Modules:\n{available_list}\n{separator}")

#         # Get user input and validate.
#         while True:
#             chosen_input = input("\nEnter the python modules you want to pull (comma-separated): ").strip()
#             if not chosen_input:
#                 print("No modules selected. Please try again.")
#                 continue
                
#             chosen_modules = [doc.strip() for doc in chosen_input.split(',')]
#             invalid_folders = [doc for doc in chosen_modules if doc not in self.available_modules.keys()]
            
#             if invalid_folders:
#                 print(f"Invalid folder(s): {', '.join(invalid_folders)}\nPlease try again.")
#                 continue
#             break

#         # Create the output dictionary.
#         # chosen_modules = {
#         #     key: value for key, value in chosen_modules 
#         #     if key in self.available_modules.keys()
#         # }

#         chosen_modules = {
#             module: self.available_modules[module] 
#             for module in chosen_modules 
#             if module in self.available_modules
#         }

#         # Always include the required folders
#         for key in self.always_include:
#             if key not in chosen_modules:
#                 chosen_modules[key] = self.available_modules[key]

#         print(f"chosen modules: {chosen_modules}")
#         return chosen_modules

class ChooseModule:


    def __init__(self, always_include: Optional[list[str]] = None) -> None:
        self.yaml_path: Path = Path(PROJECT_ROOT) / "github_urls_for_modules.yaml"
        self.always_include: list[str] = [module.lower() for module in (always_include or [])]
        self.top_level_dir: list[str] = os.listdir(CUSTOM_MODULES_FOLDER)
        
        # Load GitHub URLs
        self.github_urls: dict[str, str] = self._load_github_urls()
        
        # Get available modules
        self.modules_available_on_github: dict[str, str] = self._get_modules_that_are_available_on_github()
        self.modules_available_on_disk: dict[str, str] = self._get_modules_that_are_available_on_disk()
        logger.debug(f"self.modules_available_on_github:\n{self.modules_available_on_github}", f=True)
        logger.debug(f"self.modules_available_on_disk:\n{self.modules_available_on_disk}", f=True)
        
        # Combine available modules
        self.available_modules: dict[str, str] = {
            k.lower(): v for k, v in {
                **self.modules_available_on_disk,
                **self.modules_available_on_github
            }.items()
        }
        logger.debug(f"self.available_modules:\n{self.available_modules}", f=True)


    def _load_github_urls(self) -> dict[str, str]:
        """Load and validate GitHub URLs from YAML file."""
        try:
            with open(self.yaml_path) as f:
                urls = yaml.safe_load(f)
            
            if not isinstance(urls, dict):
                raise ValueError("YAML file must contain a dictionary")
            
            return urls
        except Exception as e:
            logger.warning(f"Could not import URL yaml file: {e}")
            return {"_default": "_option"}


    def _get_modules_that_are_available_on_github(self) -> dict[str, str]:
        """Create a dictionary of modules that are available on github."""
        return dict(self.github_urls)


    def _get_modules_that_are_available_on_disk(self) -> dict[str, str]:
        """Get all valid module folders from disk."""
        if not os.path.isdir(CUSTOM_MODULES_FOLDER):
            logger.warning(f"Custom modules folder not found: {CUSTOM_MODULES_FOLDER}")
            return {}

        # Get module folders excluding those available on GitHub
        base_path = Path(CUSTOM_MODULES_FOLDER)
        subfolders = {}

        for dir in base_path.iterdir():
            for d in dir.iterdir():
                if not d.is_dir():
                    continue

                name = d.name.lower()
                if name in self.modules_available_on_github or name in self.top_level_dir:
                    continue

                subfolders[d.name] = str(d)

        # Remove OS-specific folders
        if os.name == 'nt':
            subfolders.pop('bash', None)
            logger.debug("Removed 'bash' folder for Windows")
        else:
            subfolders.pop('batch', None)
            logger.debug("Removed 'batch' folder for non-Windows")

        logger.debug(f"Final subfolders: {subfolders}")
        return subfolders


    def modules(self) -> dict[str, str]:
        """Let user choose which modules to use and include required ones."""
        # Display available modules
        available_modules = sorted(
            module for module in self.available_modules
            if module not in self.always_include
        )

        separator = "*" * 20
        module_list = "\n".join(f"- {module}" for module in available_modules)
        always_include_list = "\n".join(f"- {module}" for module in self.always_include)
        print(f"{separator}\nAvailable Modules:\n{module_list}\n{separator}")
        print(f"Always Included:\n{always_include_list}\n{separator}")

        # Get and validate user input
        while True:
            chosen_input = input("\nEnter the python modules you want to pull (comma-separated): ").strip()
            if not chosen_input:
                print("No modules selected. Please try again.")
                continue

            chosen_modules = [module.strip().lower() for module in chosen_input.split(',')]
            logger.debug(f"chosen_modules\n{chosen_modules}",f=True)
            invalid_modules = [module for module in chosen_modules if module not in self.available_modules]
            
            if invalid_modules:
                print(f"Invalid module(s): {', '.join(invalid_modules)}\nPlease try again.")
                continue
            
            break

        # Create final module selection including required modules
        selected_modules = {
            module: self.available_modules[module]
            for module in set(chosen_modules + self.always_include)
        }

        logger.debug(f"Selected modules: {selected_modules}")
        return selected_modules

