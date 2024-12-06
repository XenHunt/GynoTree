import os


def _get_env_variable(name, var_type, default=None):
    try:
        value = os.environ[name]
        return var_type(value)
    except KeyError:
        return default


configuration = {
    "DEBUG": _get_env_variable("DEBUG", bool, False),
    "DB": {
        "HOST": _get_env_variable("DB_HOST", str, "localhost"),
        "NAME": _get_env_variable("DB_NAME", str, "db"),
        "USER": _get_env_variable("DB_USER", str, "root"),
        "PORT": _get_env_variable("DB_PORT", int, 3306),
        "PASSWORD": _get_env_variable("DB_PASSWORD", str, ""),
    },
}
