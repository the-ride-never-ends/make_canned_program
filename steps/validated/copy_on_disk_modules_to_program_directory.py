from pathlib import Path
import shutil


from logger.logger import Logger
logger = Logger(logger_name=__name__)


class CopyOnDiskModulesToProgramDirectory:
    """Handle copying of on-disk modules to a program directory.
    
    Validates module paths and copies only disk-based modules (not GitHub URLs)
    to the specified program directory.
    """

    def __init__(self, 
                 chosen_modules: dict[str, str], 
                 program_path: str
                ) -> None:
        """Initialize with module paths and destination directory.
        
        Args:
            chosen_modules (dict[str, str]): Dictionary mapping module names to their paths.
            program_path (str): The destination directory path.
        """
        self.chosen_modules = self._validate_paths(chosen_modules)
        self.program_path = self._validate_paths(program_path)


    def _validate_path_helper(self, path: str) -> Path:
        """Validate that a path exists and is a directory.
        
        Args:
            path (str): The path to validate.
            
        Returns:
            Path: The validated Path object.
            
        Raises:
            ValueError: If the path doesn't exist or isn't a directory.
        """
        path: Path = Path(path)
        if not path.exists():
            raise ValueError(f"Path does not exist: {path}")

        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        return path


    def _validate_paths(self, path: str|dict[str, str]) -> str|dict[str, Path]:
        """
        Check to make sure paths exist and are directories.

        Args:
            path (str | dict[str, str]): The path or dictionary of paths to validate.

        Returns:
            str | dict[str, Path]: The validated path(s). If a dictionary was
            provided, returns a new dictionary with validated Path objects as values.

        Raises:
            ValueError: If a path does not exist or is not a directory.
        """
        if isinstance(path, dict):
            _path = {}
            # Validate the path of each module.
            for module_name, module_path in path.items():
                # Skip URLs - they'll be handled elsewhere
                if str(module_path).startswith(("http://", "https://")):
                    logger.debug(f"Skipping github module: {module_name}")
                else:
                    _path.update({module_name: self._validate_path_helper(module_path)})
            # Overwrite the original dictionary with the validated paths.
            path = _path
        else:
            path = self._validate_path_helper(path)
        return path

    def modules_to_program_directory(self) -> None:
        """
        Copy local modules to the program path, skipping any modules that are URLs.
        
        Args:
            chosen_modules: dictionary mapping module names to their paths/URLs
            program_path: Destination directory where modules should be copied
        
        Raises:
            OSError: If there are permission issues or I/O errors during copying
            ValueError: If the program path doesn't exist or isn't a directory
        """
        for module_name, module_path in self.chosen_modules.items():
            try:
                # Get the destination path.
                destination_path: Path = self.program_path / module_name

                # Throw an error if it already exists.
                if destination_path.exists():
                    logger.debug(f"Module already exists at: {destination_path}")
                    raise FileExistsError(f"Module already exists at: {destination_path}")
                
                # Copy the module directory.
                logger.info(f"Copying module '{module_name}' from {module_path} to {destination_path}")
                shutil.copytree(
                    module_path,
                    destination_path,
                    symlinks=True,
                    ignore=shutil.ignore_patterns('*.pyc', '__pycache__', '.git', '.github', '.pytest_cache'),
                    dirs_exist_ok=True
                )
                logger.info(f"Successfully copied module: {module_name}")

            except PermissionError as e:
                logger.error(f"Permission denied while copying module '{module_name}': {e}")
                raise OSError(f"Permission denied while copying module '{module_name}'") from e

            except OSError as e:
                logger.error(f"Error copying module '{module_name}': {e}")
                raise OSError(f"Failed to copy module '{module_name}'") from e

