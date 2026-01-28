from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CustomEventsRequest(BaseModel):
    season_uuid: UUID

class EventResponse(BaseModel):
    uuid: UUID
    season: UUID
    event_code: str
    name: str
    type: str
    city: str
    country: str
    start_date: str
    end_date: str
    pits_generated: bool
    custom: bool
    created_at: datetime

class CustomEventRequest(BaseModel):
    season_uuid: UUID
    event_code: str
    event_name: str
    event_type: str
    event_city: str
    event_country: str
    event_start_date: str
    event_end_date: str