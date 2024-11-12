import os
import stat

from logger.logger import Logger
logger = Logger(logger_name=__name__)

def remove_readonly(func, path, exc_info):
    """"
    Clear the readonly bit and reattempt the removal
    See: https://github.com/python/cpython/issues/87823
    """
    # ERROR_ACCESS_DENIED = 5
    if func not in (os.unlink, os.rmdir) or exc_info[1].winerror != 5:
        logger.error(f"Failed to remove {path} with error {exc_info[1]}")
        raise exc_info[1]
    logger.error(f"Encountered Read-only Bit. Changing...")
    os.chmod(path, stat.S_IWRITE)
    func(path)

