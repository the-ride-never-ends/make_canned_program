"""
Git Module Puller

This module provides functionality to pull and manage Git modules from GitHub repositories.

It includes a GitModulePuller class that handles operations such as pulling modules,
checking their status, and updating module URLs. The module also includes utility
functions for pulling requested modules from GitHub based on user input.

The main components of this module are:
- GitModulePuller class: Manages Git operations for pulling modules
- pull_requested_modules_from_github function: Interactively pulls requested modules
- GITHUB_URLS_FOR_MODULES: Dictionary mapping module names to their GitHub URLs

This module relies on configuration from the project's config module and uses
the custom logger for logging operations.
"""

import os
import subprocess


import yaml


from config.config import PROJECT_ROOT, PULLED_REPOS_PATH
from logger.logger import Logger
logger = Logger(logger_name=__name__)

GITHUB_URLS_FOR_MODULES = {
    "database": "https://github.com/the-ride-never-ends/database",
    "config": "https://github.com/the-ride-never-ends/config",
    "utils": "https://github.com/the-ride-never-ends/utils",
    "logger": "https://github.com/the-ride-never-ends/logger",
    "llm_engine": "https://github.com/the-ride-never-ends/llm_engine",
    "api": "https://github.com/the-ride-never-ends/api",
    "main": "https://github.com/the-ride-never-ends/main"
}
GITHUB_URLS_FOR_MODULES_PATH = os.path.join(PROJECT_ROOT, "github_urls_for_modules.yaml")


class GitModulePuller:
    """
    A utility class to manage Git operations for pulling modules from GitHub.
    """
    def __init__(self):
        """
        Initialize the GitModulePuller.
        
        Args:
            base_path: The base directory where modules will be cloned
            github_urls: Dictionary mapping module names to their GitHub URLs
        """
        self.logger = logger
        self.github_urls: dict = None
        # Import the GITHUB_URLS_FOR_MODULES dictionary from the YAML file.
        # Else, use the default dictionary defined above.
        try:
            with open(GITHUB_URLS_FOR_MODULES_PATH, "r") as file:
                self.github_urls = yaml.load(file)
        except FileNotFoundError:
            self.logger.error(f"GitHub URLs file not found at {GITHUB_URLS_FOR_MODULES_PATH}\n Defaulting to presest...")
            self.github_urls = GITHUB_URLS_FOR_MODULES

    def _run_git_command(self, command: list, cwd: str = None) -> tuple[bool, str]:
        """
        Execute a git command and return the result.
        
        Args:
            command: List of command components
            cwd: Working directory for the command
            
        Returns:
            Tuple of (success boolean, output/error message)
        """
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, f"Git command failed: {e.stderr}"
        except Exception as e:
            return False, f"Error executing git command: {e}"
    
    def pull_module(self, module_name: str) -> tuple[bool, str, str]:
        """
        Pull a specific module from GitHub.
        If the module directory doesn't exist yet, clone the repos from GitHub

        Args:
            module_name: Name of the module to pull
            
        Returns:
            Tuple of (success boolean, status message)
        """
        if module_name not in self.github_urls:
            return False, f"Module {module_name} not found in configured GitHub URLs"
        
        module_path = os.path.join(PULLED_REPOS_PATH, module_name)
        url = self.github_urls[module_name]
        
        # If directory exists, pull latest changes
        if os.path.exists(module_path):
            self.logger.info(f"Pulling latest changes for {module_name}")
            success, message = self._run_git_command(
                ['git', 'pull', 'origin', 'main'],
                cwd=module_path
            )
            if not success:
                # Try master branch if main fails
                success, message = self._run_git_command(
                    ['git', 'pull', 'origin', 'master'],
                    cwd=module_path
                )
        # If directory doesn't exist, clone the repository
        else:
            self.logger.info(f"Cloning {module_name} from {url}")
            success, message = self._run_git_command(
                ['git', 'clone', url, module_path]
            )
        
        return module_name, success, message
    
    # def pull_requested_modules(self, module_list: list) -> dict[str, tuple[bool, str]]:
    #     """
    #     Pull requested modules from GitHub.
        
    #     Returns:
    #         Dictionary mapping module names to their (success, message) tuples
    #     """
    #     output_dict = {}
    #     for module_name in module_list:
    #         # Skip unavailable modules
    #         module_name: str
    #         available = module_name in GITHUB_URLS_FOR_MODULES
    #         if not available:
    #             logger.warning(f"'{module_name}' module not in yaml or defaults. Skipping...")
    #             continue

    #         # Try to pull the module. If successful, add to output_dict
    #         success, module_name, message = self.pull_module(module_name)
    #         output_dict[module_name] = (success, message)
    #         if success:
    #             logger.info(f"'{module_name}' module pulled successfully.")
    #         else:
    #             logger.error(f"'{module_name}' module failed to import: {message}.")
    #     return output_dict


    def get_module_status(self, module_name: str) -> tuple[bool, str]:
        """
        Get the current git status of a module.
        
        Args:
            module_name: Name of the module to check
            
        Returns:
            Tuple of (success boolean, status message)
        """
        module_path = os.path.join(PULLED_REPOS_PATH, module_name)
        
        if not os.path.exists(module_path):
            return False, f"Module {module_name} is not cloned yet"
        
        return self._run_git_command(['git', 'status'], cwd=module_path)

    def update_module_url(self, module_name: str, new_url: str) -> None:
        """
        Update the GitHub URL for a module.
        
        Args:
            module_name: Name of the module to update
            new_url: New GitHub URL for the module
        """
        self.github_urls[module_name] = new_url


def pull_requested_modules_from_github():

    # Format the list of available modules as a string
    requested_module_list = []
    module_list = "\n".join([key for key in GITHUB_URLS_FOR_MODULES.keys()])
    asterisk_x_20 = "*" * 20
    print(f"{asterisk_x_20}**Available modules**{module_list}{asterisk_x_20}")

    # Ask the user for the modules they want to include in their project
    for module in GITHUB_URLS_FOR_MODULES.keys():
        # Auto-include logger, config, utils, and main modules
        if module in ["logger", "config", "utils", "main"]:
            requested_module_list.append(module)
            print(f"Automatically added the '{module}' module.")
        else:
            # Ask the user if they want to include the module
            include_module = input(f"Do you want to include the '{module}' module? (y/n): ").lower()
            if include_module == "y":
                requested_module_list.append(module)

    results = {}
    # Initialize the puller
    puller = GitModulePuller()
    for module_name in requested_module_list:
        # Try to pull the module from github and add it to the output dictionary.
        try:
            results[module_name] = puller.pull_module(module_name) # -> tuple[bool, str, str]
            logger.info(f"'{module_name}' module pulled successfully.")
        except:
            results[module_name] = (False, "Failed to pull module")

    # Print the results
    for module_name, (success, message) in results.items():
        logger.info(f"{module_name}: {'Success' if success else 'Failed'} - {message}")


