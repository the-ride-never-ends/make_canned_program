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
from pathlib import Path
import shutil
import subprocess
import time
import tempfile


from config.config import PROJECT_ROOT, PULLED_REPOS_PATH
from logger.logger import Logger
logger = Logger(logger_name=__name__)


class PullRemoteModulesFromGithub:
    """
    A utility class to manage Git operations for pulling modules from GitHub.
    """
    def __init__(self, chosen_modules: dict[str, str], program_path: str):
        """
        Initialize the GitModulePuller.
        
        Args:
            base_path: The base directory where modules will be cloned
            github_urls: Dictionary mapping module names to their GitHub URLs
        """
        self.chosen_modules: dict[str, str] = self._remove_on_disk_custom_modules(chosen_modules)
        # NOTE We don't need to validate program_path since it was already validated in the previous step.
        self.program_path: str = program_path 
        self.github_urls: dict = None


    def remote_modules_from_github(self) -> None:

        results = {}
        for module_name in self.chosen_modules.keys():
            # Try to pull the module from github and add it to the output dictionary.
            try:
                results[module_name] = self._pull_module(module_name) # -> tuple[bool, str, str]
                logger.info(f"'{module_name}' module pulled successfully.")
            except:
                results[module_name] = (False, "Failed to pull module")

        # Print the results
        for module_name, tup in results.items():
            _, success, message = tup
            logger.info(f"{module_name}: {'Success' if success else 'Failed'} - {message}")


    def _remove_on_disk_custom_modules(self, path: str|dict[str, str]) -> str|dict[str, Path]:
        github_modules = {}
        for module_name, module_path in path.items():
            if str(module_path).startswith(("http://", "https://")):
                logger.debug(f"Github module: {module_name}")
                github_modules.update({module_name: module_path})
        return github_modules


    def _run_git_command(self, command: list, cwd: str = None, 
                         max_attempts: int = 3, delay: int = 1) -> tuple[bool, str]:
        """
        Execute a git command and return the result.
        
        Args:
            command: List of command components
            cwd: Working directory for the command
            
        Returns:
            Tuple of (success boolean, output/error message)
        """
        for attempt in range(max_attempts):
            try:
                result = subprocess.run(
                    command,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return True, result.stdout
            except PermissionError:
                if attempt == max_attempts - 1:
                    raise
                time.sleep(delay)
                continue
            except subprocess.CalledProcessError as e:
                return False, f"Git command failed: {e.stderr}"
            except Exception as e:
                return False, f"Error executing git command: {e}"


    def _pull_module(self, module_name: str) -> tuple[bool, str, str]:
        """
        Pull a specific module from GitHub.
        Clone the repos from GitHub to a temporary directory,
        then move it to the final destination if successful.

        Args:
            module_name: Name of the module to pull
            
        Returns:
            Tuple of (success boolean, status message)
        """
        if module_name not in self.chosen_modules:
            return False, f"Module {module_name} not found in configured GitHub URLs"

        final_module_path = os.path.join(self.program_path, module_name)
        url = self.chosen_modules[module_name]

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_module_path = os.path.join(temp_dir, module_name)

            logger.info(f"Cloning {module_name} from {url} to temporary directory")
            success, message = self._run_git_command(
                ['git', 'clone', url, temp_module_path]
            )
            if success:
                # If cloning was successful, move the temporary directory to the final location
                try:
                    if os.path.exists(final_module_path):
                        shutil.rmtree(final_module_path)
                    shutil.move(temp_module_path, final_module_path)
                    logger.info(f"Successfully moved {module_name} to {final_module_path}")
                except Exception as e:
                    success = False
                    message = f"Failed to move temporary directory to final location: {e}"
                    logger.error(message)
            return module_name, success, message


    # def _get_module_status(self, module_name: str) -> tuple[bool, str]:
    #     """
    #     Get the current git status of a module.
        
    #     Args:
    #         module_name: Name of the module to check
            
    #     Returns:
    #         Tuple of (success boolean, status message)
    #     """
    #     module_path = os.path.join(self.program_path, module_name)
        
    #     if not os.path.exists(module_path):
    #         return False, f"Module {module_name} is not cloned yet"
        
    #     success, output = self._run_git_command(['git', 'status'], cwd=module_path)
    #     if not success:
    #         raise Exception(f"Failed to get git status for module {module_name}: {output}")





