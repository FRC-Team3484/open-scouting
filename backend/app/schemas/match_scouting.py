from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class MatchScoutingRequest(BaseModel):
    submission_uuid: UUID
    fields: dict[Any, Any]
    user_uuid: UUID | str # Is either the UUID for the authenticated user, or just a username
    year: int
    team_number: int
    match_number: int
    match_type: str
    event_code: str

class MatchScoutingResponse(BaseModel):
    uuid: UUID
    user: UUID | None
    event: UUID
    team_number: int
    match_number: int
    match_type: str
    created_at: datetime

class SubmissionResponse(BaseModel):
    uuid: UUID
    event_name: str
    event_code: str
    team_number: int
    match_number: int
    match_type: str
    answers: int
    created_at: datetime