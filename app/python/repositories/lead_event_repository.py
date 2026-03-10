# Repository responsible for persisting lead lifecycle events into the Snowflake ANALYTICS.LEAD_EVENTS table.
# -- ======================================================
import pandas as pd
from typing import Iterable
from utils.logger import get_logger

logger = get_logger(__name__)


class LeadEventRepository:
  
  #  Data access layer responsible for writing lifecycle events to Snowflake.
  

    TARGET_TABLE = "LEADS_DB.ANALYTICS.LEAD_EVENTS"
    INSERT_BATCH_SIZE = 1000

    def __init__(self, connection) -> None:
      
      #  Initialize repository with an active Snowflake connection.
       
        self._connection = connection

    def replace_events(self, events_df: pd.DataFrame) -> None:
        
      #  Replace lifecycle events in Snowflake with the provided dataset.

        if events_df.empty:
            logger.warning("No lifecycle events to insert.")
            return

        try:
            logger.info("Preparing lifecycle events for persistence")

            # Ensure datetime columns are properly formatted
            events_df["EVENT_DATE"] = pd.to_datetime(
                events_df["EVENT_DATE"], errors="coerce"
            )

            events_df["UPDATED_DATE_UTC"] = pd.to_datetime(
                events_df["UPDATED_DATE_UTC"], errors="coerce"
            )

            with self._connection.cursor() as cursor:

                logger.info("Clearing existing events table: %s", self.TARGET_TABLE)

                cursor.execute(f"TRUNCATE TABLE {self.TARGET_TABLE}")

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
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                rows = self._prepare_rows(events_df)

                logger.info("Inserting %s lifecycle events", len(rows))

                # Insert rows in batches for better scalability
                for batch in self._chunk_rows(rows, self.INSERT_BATCH_SIZE):
                    cursor.executemany(insert_sql, batch)

                self._connection.commit()

                logger.info("Lifecycle events successfully written to Snowflake")

        except Exception as exc:
            logger.error("Failed to persist lifecycle events: %s", exc)

            self._connection.rollback()

            raise

    def _prepare_rows(self, df: pd.DataFrame) -> list[tuple]:
      
       # Convert DataFrame rows into Snowflake-compatible tuples.
    

        rows = []

        for row in df.itertuples(index=False):

            rows.append(
                (
                    row.ID,
                    row.EVENT_TYPE,
                    row.EVENT_EMPLOYEE,
                    None
                    if pd.isna(row.EVENT_DATE)
                    else row.EVENT_DATE.to_pydatetime(),
                    row.LEAD_ID,
                    None
                    if pd.isna(row.UPDATED_DATE_UTC)
                    else row.UPDATED_DATE_UTC.to_pydatetime(),
                )
            )

        return rows

    def _chunk_rows(self, rows: list[tuple], size: int) -> Iterable[list[tuple]]:
       
      #  Yield row batches for scalable batch insertion.
   

        for i in range(0, len(rows), size):
            yield rows[i : i + size]