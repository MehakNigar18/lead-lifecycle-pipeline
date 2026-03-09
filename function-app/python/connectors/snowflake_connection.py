
# Manages Snowflake database connections.

import snowflake.connector
from snowflake.connector import SnowflakeConnection as SnowflakeConn
from config.settings import Settings
import logging

logger = logging.getLogger(__name__)


class SnowflakeConnection:


    def __init__(self) -> None:
        self._connection: SnowflakeConn | None = None

    def connect(self) -> SnowflakeConn:
       
      #  Establish a connection to Snowflake.


        try:
            logger.info("Connecting to Snowflake account: %s", Settings.SNOWFLAKE_ACCOUNT)

            self._connection = snowflake.connector.connect(
                user=Settings.SNOWFLAKE_USER,
                password=Settings.SNOWFLAKE_PASSWORD,
                account=Settings.SNOWFLAKE_ACCOUNT,
                warehouse=Settings.SNOWFLAKE_WAREHOUSE,
                database=Settings.SNOWFLAKE_DATABASE,
                schema=Settings.SNOWFLAKE_SCHEMA_RAW,
            )

            logger.info("Snowflake connection established successfully")
            return self._connection

        except Exception as exc:
            logger.error("Failed to connect to Snowflake: %s", exc)
            raise

    def close(self) -> None:
        """
        Close the Snowflake connection safely.
        """

        if self._connection:
            self._connection.close()
            logger.info("Snowflake connection closed")