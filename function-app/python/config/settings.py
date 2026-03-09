# Load environment variables from the .env file into the application
# This allows sensitive credentials (like Snowflake passwords) to be stored

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")

    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")

    # schemas
    SNOWFLAKE_SCHEMA_RAW = os.getenv("SNOWFLAKE_SCHEMA_RAW", "RAW")
    SNOWFLAKE_SCHEMA_ANALYTICS = os.getenv("SNOWFLAKE_SCHEMA_ANALYTICS", "ANALYTICS")