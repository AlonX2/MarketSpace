def _setup_logger():
    """
    Setups logging for the vectorspace_driver package.
    """

    import logging
    from utils import setup_logger

    logger = logging.getLogger(__package__)
    logger.name = "collector"
    setup_logger(logger)

_setup_logger()