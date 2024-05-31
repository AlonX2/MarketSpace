import os

class MissingEnvironmentVariableError(Exception):
    """
    Error for when an environment variable is missing.
    """
    pass

def get_env_vars(env_var_names: list[str], required: bool = False) -> list[str]:
    """
    Attempts to fetch multiple requested environment variable values.
    :param env_var_names: The env vars to fetch.
    :param required: Wheter the function should error in case of a missing var. 
                     If False, the value of any missing vars will be None.
    :returns: list of the found env var values, in the same order as the one in the input list.
    """

    values = []
    for var in env_var_names:
        if var not in os.environ and required:
            raise MissingEnvironmentVariableError(f"Required env var '{var}' is missing.")
        
        values.append(os.getenv(var))
    
    return values