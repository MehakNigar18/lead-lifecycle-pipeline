
 # Snowflake connection manager.

 # Responsible for establishing and safely managing connections to the Snowflake data warehouse.
 # ======================================================

import snowflake.connector
from snowflake.connector import SnowflakeConnection as SnowflakeConn

from app.python.config.settings import settings
from utils.logger import get_logger
# Initialize project logger
logger = get_logger(__name__)


class SnowflakeConnection:

    def __init__(self) -> None:
        # Internal Snowflake connection instance
        self._connection: SnowflakeConn | None = None

    def connect(self) -> SnowflakeConn:

        # Reuse existing connection if already established
        if self._connection:
            logger.debug("Reusing existing Snowflake connection")
            return self._connection

        try:
            logger.info("Establishing connection to Snowflake")

            self._connection = snowflake.connector.connect(
                user=settings.SNOWFLAKE_USER,
                password=settings.SNOWFLAKE_PASSWORD,
                account=settings.SNOWFLAKE_ACCOUNT,
                warehouse=settings.SNOWFLAKE_WAREHOUSE,
                database=settings.SNOWFLAKE_DATABASE,
                schema=settings.SNOWFLAKE_SCHEMA_RAW,
            )

            logger.info("Snowflake connection established successfully")

            return self._connection

        except Exception as exc:
            logger.error("Snowflake connection failed: %s", exc)
            raise

    def close(self) -> None:
       
      #  Safely close the Snowflake connection.
      
        if self._connection:
            try:
                self._connection.close()
                logger.info("Snowflake connection closed")

            except Exception as exc:
                logger.warning(
                    "Error while closing Snowflake connection: %s", exc
                )

            finally:
                # Reset connection reference
                self._connection = None