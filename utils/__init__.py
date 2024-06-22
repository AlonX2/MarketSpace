from .env import *
from .logging import *

def _setup_logger():
    """
    Setups logging for the vectorspace_driver package.
    """

    import logging
    logger = logging.getLogger(__package__)
    logger.name = "utils"
    setup_logger(logger=logger)

_setup_logger()