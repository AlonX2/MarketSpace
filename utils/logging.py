import logging

def setup_logger():
    """
    Setups logging.
    """
    logger = logging.getLogger(__package__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s]:  %(message)s')

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