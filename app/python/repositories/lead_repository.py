
# Repository responsible for retrieving lead data from the Snowflake RAW.LEADS table.


import pandas as pd
from utils.logger import get_logger

# Initialize module logger
logger = get_logger(__name__)


class LeadRepository:
    """
    Data access layer for retrieving lead records from Snowflake.
    """

    # SQL query used to retrieve lead data
    # Explicit column selection avoids schema surprises and improves performance
    QUERY_FETCH_LEADS = """
        SELECT
            l.ID,
            l.STATE,
            l.CREATEDDATEUTC,
            l.CANCELLATIONREQUESTDATEUTC,
            l.CANCELLATIONDATEUTC,
            l.CANCELLATIONREJECTIONDATEUTC,
            l.SOLDEMPLOYEE,
            l.CANCELEDEMPLOYEE,
            l.UPDATEDDATEUTC
        FROM LEADS_DB.RAW.LEADS l
        ORDER BY l.CREATEDDATEUTC
    """

    def __init__(self, connection) -> None:
    
        self._connection = connection

    def fetch_leads(self) -> pd.DataFrame:
      
       # Retrieve lead records from Snowflake.

       

        try:
            logger.info("Fetching leads from Snowflake table LEADS_DB.RAW.LEADS")

            # Execute SQL query and load results into DataFrame
            leads_df = pd.read_sql_query(self.QUERY_FETCH_LEADS, self._connection)

            logger.info("Successfully fetched %s leads", len(leads_df))

            return leads_df

        except Exception as exc:
            logger.error("Failed to fetch leads from Snowflake: %s", exc)
            raise