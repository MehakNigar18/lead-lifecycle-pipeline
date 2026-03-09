# Verbund Pflegehilfe Data Engineering Task
# Author: Mehak Nigar


"""
 ---  Lead Lifecycle Transformation Pipeline -----

This script orchestrates the full data pipeline:

1. Connect to Snowflake
2. Extract leads data from the LEADS table
3. Transform the data into lifecycle events
4. Load the events into the LEAD_EVENTS table

---  Architecture:
Snowflake (LEADS) → Python Transformation → Snowflake (LEAD_EVENTS) → Power BI
"""

import logging
from app.python.connectors.snowflake_connection import SnowflakeConnection
from app.python.repositories.lead_repository import LeadRepository
from app.python.repositories.lead_event_repository import LeadEventRepository
from app.python.services.lead_event_transformer import LeadEventTransformer
from app.python.repositories.lead_event_repository import LeadEventRepository

 # Logging Configuration 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:

    logger.info("Starting Lead lifecycle transformation pipeline...")

    # Connect to Snowflake
    connection = SnowflakeConnection().connect()
    # Initialize repositories
    lead_repo = LeadRepository(connection)
    event_repo = LeadEventRepository(connection)
    # Initialize transformation service
    transformer = LeadEventTransformer()

    # Fetch leads
    leads_df = lead_repo.fetch_leads()
    logger.info(f"Fetched {len(leads_df)} leads from Snowflake")

    # Transform events
    events_df = transformer.transform(leads_df)
    logger.info(f"Generated {len(events_df)} lifecycle events")

    # Write to Snowflake
    event_repo.replace_events(events_df)

    logger.info("Transformation completed successfully.")


if __name__ == "__main__":
    main()