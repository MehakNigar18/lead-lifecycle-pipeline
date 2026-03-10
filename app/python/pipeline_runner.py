# Verbund Pflegehilfe Data Engineering Task
# Author: Mehak Nigar


# Lead Lifecycle Transformation Pipeline

# This module orchestrates the full data pipeline:

# 1. Connect to Snowflake
# 2. Extract leads data from the LEADS table
# 3. Transform leads into lifecycle events
# 4. Load lifecycle events into the LEAD_EVENTS table

## Architecture:
#Snowflake (LEADS) → Python Transformation → Snowflake (LEAD_EVENTS) → Power BI


from app.python.connectors.snowflake_connection import SnowflakeConnection
from app.python.repositories.lead_repository import LeadRepository
from app.python.repositories.lead_event_repository import LeadEventRepository
from app.python.services.lead_event_transformer import LeadEventTransformer
from utils.logger import get_logger


logger = get_logger(__name__)


def main() -> None:
    
   # Execute the Lead Lifecycle Transformation Pipeline.
   

    logger.info("Starting Lead Lifecycle Transformation Pipeline")

    try:
        # ---------------------------
        # Step 1: Connect to Snowflake
        # ---------------------------
        logger.info("Establishing Snowflake connection")

        connection = SnowflakeConnection().connect()

        # ---------------------------
        # Step 2: Initialize components
        # ---------------------------
        lead_repository = LeadRepository(connection)
        lead_event_repository = LeadEventRepository(connection)
        transformer = LeadEventTransformer()

        # ---------------------------
        # Step 3: Extract
        # ---------------------------
        logger.info("Fetching leads from Snowflake")

        leads_df = lead_repository.fetch_leads()

        logger.info("Fetched %s leads", len(leads_df))

        # ---------------------------
        # Step 4: Transform
        # ---------------------------
        logger.info("Transforming leads into lifecycle events")

        events_df = transformer.transform(leads_df)

        logger.info("Generated %s lifecycle events", len(events_df))

        # ---------------------------
        # Step 5: Load
        # ---------------------------
        logger.info("Loading lifecycle events into LEAD_EVENTS table")

        lead_event_repository.replace_events(events_df)

        # ---------------------------
        # Pipeline Metrics
        # ---------------------------
        logger.info(
            "Pipeline completed successfully | leads_processed=%s events_generated=%s",
            len(leads_df),
            len(events_df),
        )

    except Exception as error:
        logger.exception("Lead Lifecycle Transformation Pipeline failed")
        raise error


if __name__ == "__main__":
    main()