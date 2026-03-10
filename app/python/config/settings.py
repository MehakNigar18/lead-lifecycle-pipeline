
# Application configuration module.

import os
from dotenv import load_dotenv
from dataclasses import dataclass


# Load environment variables from .env (local development)
load_dotenv()


def _get_env_variable(name: str, default: str | None = None) -> str:
 
   #  Safely fetch environment variables.

    value = os.getenv(name, default)

    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {name}")

    return value


@dataclass(frozen=True)
class Settings:
   
   # Using dataclass ensures structured configuration  and prevents accidental mutation during runtime.


    # Snowflake authentication
    SNOWFLAKE_ACCOUNT: str = _get_env_variable("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_USER: str = _get_env_variable("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD: str = _get_env_variable("SNOWFLAKE_PASSWORD")

    # Snowflake compute
    SNOWFLAKE_WAREHOUSE: str = _get_env_variable("SNOWFLAKE_WAREHOUSE")
    SNOWFLAKE_DATABASE: str = _get_env_variable("SNOWFLAKE_DATABASE")

    # Snowflake schemas
    SNOWFLAKE_SCHEMA_RAW: str = os.getenv("SNOWFLAKE_SCHEMA_RAW", "RAW")
    SNOWFLAKE_SCHEMA_ANALYTICS: str = os.getenv("SNOWFLAKE_SCHEMA_ANALYTICS", "ANALYTICS")


# Create a singleton instance of settings
settings = Settings()