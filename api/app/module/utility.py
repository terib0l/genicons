import os
import logging

logger = logging.getLogger("genicons")

def remove_file(
        path: str = None,
        paths: list = None
    ):
    logger.info(remove_file.__name__)
    if path:
        logger.debug(path)
        if os.path.isfile(path): os.remove(path)

    if paths:
        logger.debug(paths)
        for p in paths:
            if os.path.isfile(p): os.remove(p)
