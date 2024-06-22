import logging

def setup_logger(logger: logging.Logger):
    """
    Setups a logger.
    """
    logging.basicConfig()
    
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s]:  %(message)s', datefmt="%d/%m/%Y %I:%M:%S %p %Z")

    ch.setFormatter(formatter)

    logger.addHandler(ch)

def format_logged_substring(string: str) -> str:
    """
    Used to format the length of a substring that is logged as part of a larger log.
    :param string: The logged string.
    :returns: A formatted and possibly shorter version of the string.
    """
    MAX_SUBSTRING_LENGTH = 30
    return f"'{string[:MAX_SUBSTRING_LENGTH]}...'"