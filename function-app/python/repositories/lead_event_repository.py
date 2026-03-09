#Repository responsible for persisting lead lifecycle events into the Snowflake ANALYTICS.LEAD_EVENTS table.

import logging
import pandas as pd
from typing import Optional


logger = logging.getLogger(__name__)

class LeadEventRepository:

    TARGET_TABLE = "LEADS_DB.ANALYTICS.LEAD_EVENTS"

    def __init__(self, connection) -> None:
        
      #  Initialize repository with an active Snowflake connection.

        self._connection = connection

    def replace_events(self, events_df: pd.DataFrame) -> None:
        """
        Replace lifecycle events in Snowflake with the transformed dataset.

        This method performs the following steps:
        1. Clears the existing LEAD_EVENTS table.
        2. Converts datetime columns to valid Python datetime objects.
        3. Inserts the new lifecycle events using batch execution.

        Parameters
        ----------
        events_df : pandas.DataFrame
            DataFrame containing lifecycle events ready for persistence.
        """

        if events_df.empty:
            logger.warning("No lifecycle events to insert.")
            return

        cursor = self._connection.cursor()

        try:
            logger.info("Clearing existing LeadEvents table...")
            cursor.execute(f"TRUNCATE TABLE {self.TARGET_TABLE}")

            logger.info("Preparing lifecycle events for insertion...")

            events_df["EVENT_DATE"] = pd.to_datetime(
                events_df["EVENT_DATE"], errors="coerce"
            )

            events_df["UPDATED_DATE_UTC"] = pd.to_datetime(
                events_df["UPDATED_DATE_UTC"], errors="coerce"
            )

            insert_sql = f"""
            INSERT INTO {self.TARGET_TABLE}
            (
                ID,
                EVENT_TYPE,
                EVENT_EMPLOYEE,
                EVENT_DATE,
                LEAD_ID,
                UPDATED_DATE_UTC
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """

            rows = [
                (
                    row.ID,
                    row.EVENT_TYPE,
                    row.EVENT_EMPLOYEE,
                    None if pd.isna(row.EVENT_DATE) else row.EVENT_DATE.to_pydatetime(),
                    row.LEAD_ID,
                    None if pd.isna(row.UPDATED_DATE_UTC) else row.UPDATED_DATE_UTC.to_pydatetime(),
                )
                for row in events_df.itertuples(index=False)
            ]

            logger.info("Inserting %s lifecycle events into Snowflake...", len(rows))

            cursor.executemany(insert_sql, rows)

            self._connection.commit()

            logger.info("Lifecycle events successfully inserted into Snowflake.")

        except Exception as exc:
            logger.error("Error inserting lifecycle events. Transaction rolled back.")
            self._connection.rollback()
            raise exc

        finally:
            cursor.close()