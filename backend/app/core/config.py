# Configuration settings for the backend
from os import getenv

class CMSettings:
    def __init__(self):
        self.CORNU_DB_URL: str = self._get_required_env("CORNU_DB_URL")

    def _get_required_env(self, var_name: str) -> str:
        value = getenv(var_name)
        if value is None:
            raise ValueError(f"environment variable {var_name} should be set.")
        return value

settings = CMSettings()
