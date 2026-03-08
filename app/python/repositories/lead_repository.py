 #  Repository responsible for retrieving lead data from the Snowflake RAW.LEADS table.

import logging
import pandas as pd

# Configure module-level logger
logger = logging.getLogger(__name__)


class LeadRepository:
  
    # SQL query used to fetch the raw leads data from Snowflake
    # Explicit column selection avoids performance issues and schema surprises.
    QUERY_FETCH_LEADS = """
        SELECT
            ID,
            STATE,
            CREATEDDATEUTC,
            CANCELLATIONREQUESTDATEUTC,
            CANCELLATIONDATEUTC,
            CANCELLATIONREJECTIONDATEUTC,
            SOLDEMPLOYEE,
            CANCELEDEMPLOYEE,
            UPDATEDDATEUTC
        FROM LEADS_DB.RAW.LEADS
    """

    def __init__(self, connection) -> None:
     
     #  Initialize repository with an active Snowflake connection.

       
        self._connection = connection

    def fetch_leads(self) -> pd.DataFrame:
        
       # Retrieve lead records from Snowflake.

       

        try:
            # Log the start of the data retrieval operation
            logger.info("Fetching leads from Snowflake table: RAW.LEADS")

            # Execute SQL query and load results into a Pandas DataFrame
            leads_df = pd.read_sql(self.QUERY_FETCH_LEADS, self._connection)

            # Log number of rows retrieved for monitoring and debugging
            logger.info("Successfully fetched %s leads from Snowflake", len(leads_df))

            return leads_df

        except Exception as exc:
            # Log the error before propagating it to the pipeline
            logger.error("Failed to fetch leads from Snowflake: %s", exc)

            # Re-raise the exception so the pipeline can handle it upstream
            raise