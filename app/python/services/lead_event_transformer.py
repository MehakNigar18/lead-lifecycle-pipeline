# Lead lifecycle transformer.
#  ======================================================
import pandas as pd
import uuid
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)


class LeadEventTransformer:
    
    # Converts raw lead records into lifecycle event records.
 
    # Mapping between lead state and lifecycle event
    STATE_EVENT_MAPPING = {
        0: "LeadSold",
        1: "LeadCancellationRequested",
        2: "LeadCancelled",
        3: "LeadCancellationRejected",
    }

    REQUIRED_COLUMNS = {
        "ID",
        "STATE",
        "CREATEDDATEUTC",
        "CANCELLATIONREQUESTDATEUTC",
        "CANCELLATIONDATEUTC",
        "CANCELLATIONREJECTIONDATEUTC",
        "SOLDEMPLOYEE",
        "CANCELEDEMPLOYEE",
    }

    def transform(self, leads_df: pd.DataFrame) -> pd.DataFrame:
     
      #  Transform raw leads dataset into lifecycle events.

        if leads_df.empty:
            logger.warning("No leads received for transformation.")
            return pd.DataFrame()

        logger.info("Starting lead lifecycle transformation")

        self._validate_schema(leads_df)

        events_df = leads_df.copy()

        # Map lifecycle state to event type
        events_df["EVENT_TYPE"] = events_df["STATE"].map(self.STATE_EVENT_MAPPING)

        # Determine event employee
        events_df["EVENT_EMPLOYEE"] = events_df["SOLDEMPLOYEE"]

        events_df.loc[
            events_df["STATE"] == 2, "EVENT_EMPLOYEE"
        ] = events_df["CANCELEDEMPLOYEE"]

        events_df["EVENT_EMPLOYEE"] = events_df["EVENT_EMPLOYEE"].fillna("Unknown")

        # Determine event date
        events_df["EVENT_DATE"] = events_df["CREATEDDATEUTC"]

        events_df.loc[
            events_df["STATE"] == 1, "EVENT_DATE"
        ] = events_df["CANCELLATIONREQUESTDATEUTC"]

        events_df.loc[
            events_df["STATE"] == 2, "EVENT_DATE"
        ] = events_df["CANCELLATIONDATEUTC"]

        events_df.loc[
            events_df["STATE"] == 3, "EVENT_DATE"
        ] = events_df["CANCELLATIONREJECTIONDATEUTC"]

        # Preserve original lead id
        events_df["LEAD_ID"] = events_df["ID"]

        # Generate unique event identifiers
        events_df["ID"] = [str(uuid.uuid4()) for _ in range(len(events_df))]

        # Pipeline processing timestamp
        events_df["UPDATED_DATE_UTC"] = datetime.utcnow()

        # Final schema selection
        events_df = events_df[
            [
                "ID",
                "EVENT_TYPE",
                "EVENT_EMPLOYEE",
                "EVENT_DATE",
                "LEAD_ID",
                "UPDATED_DATE_UTC",
            ]
        ]

        logger.info("Generated %s lifecycle events", len(events_df))

        return events_df

    def _validate_schema(self, df: pd.DataFrame) -> None:
        
      #  Validate that required columns exist in the input dataset.
        

        missing_columns = self.REQUIRED_COLUMNS - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"Missing required columns in input dataset: {missing_columns}"
            )