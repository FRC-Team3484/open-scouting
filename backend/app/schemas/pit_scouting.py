from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class SubmitPitFieldAnswerRequest(BaseModel):
    uuid: UUID
    season_uuid: UUID
    team_number: int
    event_code: str

    answers: list[Any]
    nickname: str | None

class AdminPitResponse(BaseModel):
    uuid: UUID
    event_name: str
    event_code: str
    team_number: int
    answers: int
    created_at: datetime

class PitAnswerResponse(BaseModel):
    uuid: UUID
    field_uuid: UUID
    value: str | bool | int | float
    username: str
    created_at: datetime

class GetPitsResponse(BaseModel):
    uuid: UUID
    team_number: int
    nickname: str
    created_at: datetime
    answers: list[PitAnswerResponse]
