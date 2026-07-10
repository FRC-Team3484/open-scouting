import uuid
from pydantic import BaseModel

class ServerStatusResponse(BaseModel):
    version: str | None
    active_season: uuid.UUID

class ServerStatsResponse(BaseModel):
    seasons: int
    events_scouted: int
    match_scouting_submissions: int
    pits_scouted: int