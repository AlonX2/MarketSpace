import os

class MissingEnvironmentVariableError(Exception):
    pass

def get_env_vars(env_var_names, required=False):
    values = []
    for var in env_var_names:
        if var not in os.environ and required:
            raise MissingEnvironmentVariableError(f"Required env var '{var}' is missing.")
        
        values.append(os.environ[var])
    
    return tuple(values)
        
