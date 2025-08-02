# Configuration settings for the backend
from os import getenv

# TODO: pydantic-settings for configuration management
CORNU_DB_URL = getenv("CORNU_DB_URL")
if not CORNU_DB_URL:
    raise ValueError("environment variable CORNU_DB_URL shoule be set.")
