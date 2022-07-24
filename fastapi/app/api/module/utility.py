import os
import logging

logger = logging.getLogger("genicons").getChild("utility")


def remove_file(path: str = None, paths: list = None):
    if path:
        logger.debug(f"{remove_file.__name__}, {path}")
        if os.path.isfile(path):
            os.remove(path)

    if paths:
        logger.debug(f"{remove_file.__name__}, {paths}")
        for p in paths:
            if os.path.isfile(p):
                os.remove(p)
