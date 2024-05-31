def format_logged_substring(string: str) -> str:
    """
    Used to format the length of a substring that is logged as part of a larger log.
    :param string: The logged string.
    :returns: A formatted and possibly shorter version of the string.
    """
    MAX_SUBSTRING_LENGTH = 30
    return f"'{string[:MAX_SUBSTRING_LENGTH]}...'"