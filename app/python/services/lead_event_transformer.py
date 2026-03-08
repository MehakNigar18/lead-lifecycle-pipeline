import pandas as pd
import uuid
from datetime import datetime


class LeadEventTransformer:

    STATE_EVENT_MAPPING = {
        0: "LeadSold",
        1: "LeadCancellationRequested",
        2: "LeadCancelled",
        3: "LeadCancellationRejected"
    }

    def transform(self, leads_df: pd.DataFrame) -> pd.DataFrame:

        if leads_df.empty:
            return pd.DataFrame()

        # Map state to event type
        events_df = leads_df.copy()
        events_df["EVENT_TYPE"] = events_df["STATE"].map(self.STATE_EVENT_MAPPING)

        # Determine event employee
        events_df["EVENT_EMPLOYEE"] = events_df.apply(
            lambda row: row["SOLDEMPLOYEE"] if row["STATE"] == 0
            else row["CANCELEDEMPLOYEE"] if row["STATE"] == 2
            else "Unknown",
            axis=1
        )

        # Determine event date
        events_df["EVENT_DATE"] = events_df.apply(
            lambda row: row["CREATEDDATEUTC"] if row["STATE"] == 0
            else row["CANCELLATIONREQUESTDATEUTC"] if row["STATE"] == 1
            else row["CANCELLATIONDATEUTC"] if row["STATE"] == 2
            else row["CANCELLATIONREJECTIONDATEUTC"],
            axis=1
        )

        # Generate IDs
        events_df["ID"] = [str(uuid.uuid4()) for _ in range(len(events_df))]

        # Add updated timestamp
        events_df["UPDATED_DATE_UTC"] = datetime.utcnow()

        # Rename lead id
        events_df["LEAD_ID"] = events_df["ID"]

        # Select final columns
        events_df = events_df[
            [
                "ID",
                "EVENT_TYPE",
                "EVENT_EMPLOYEE",
                "EVENT_DATE",
                "LEAD_ID",
                "UPDATED_DATE_UTC"
            ]
        ]

        return events_df