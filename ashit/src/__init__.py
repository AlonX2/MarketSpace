from utils.logging import setup_logger

def _setup_logger():
    import logging
    logger = logging.getLogger(__package__)
    logger.name = "ashit"
    setup_logger(logger)

_setup_logger()