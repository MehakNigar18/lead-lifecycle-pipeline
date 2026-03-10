 #  Domain model representing a single lead lifecycle event.

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class LeadEventModel:
    
    id: str
    event_type: str
    event_employee: Optional[str]
    event_date: datetime
    lead_id: str
    updated_date_utc: datetime

    def to_dict(self) -> Dict[str, Any]:
     
      #  Convert the event model into a dictionary compatible with Snowflake insertion or pandas DataFrame creation.
       

        return {
            "ID": self.id,
            "EVENT_TYPE": self.event_type,
            "EVENT_EMPLOYEE": self.event_employee,
            "EVENT_DATE": self.event_date,
            "LEAD_ID": self.lead_id,
            "UPDATED_DATE_UTC": self.updated_date_utc,
        }

    @staticmethod
    def now_utc() -> datetime:
      
      #  Helper method to generate a UTC timestamp. Ensures all pipeline events use a consistent timezone.
    

        return datetime.now(timezone.utc)

    def validate(self) -> None:
       
        if not self.id:
            raise ValueError("Event ID cannot be empty")

        if not self.event_type:
            raise ValueError("Event type is required")

        if not self.lead_id:
            raise ValueError("Lead ID cannot be empty")

        if not isinstance(self.event_date, datetime):
            raise ValueError("event_date must be a datetime object")