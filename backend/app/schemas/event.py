from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventResponse(BaseModel):
    uuid: UUID
    season: UUID
    event_code: str
    name: str
    type: str
    city: str
    country: str
    start_date: datetime
    end_date: datetime
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

class AdminEventResponse(EventResponse):
    match_scouting_submissions: int
    pits: int

class EventInfoResponse(BaseModel):
    match_scouting_submissions: int
    match_scouting_answers: int
    pits: int
    pit_answers: int
    pits_complete: int
    pits_incomplete: int
    pits_not_started: int