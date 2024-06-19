def _setup_logger():
    """
    Setups logging for the vectorspace_driver package.
    """
    
    import logging
    logger = logging.getLogger(__package__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s]:  %(message)s')

    ch.setFormatter(formatter)

    logger.addHandler(ch)

_setup_logger()