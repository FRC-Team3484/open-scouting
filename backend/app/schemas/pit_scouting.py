from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class PitFieldsRequest(BaseModel):
    season_uuid: UUID

class PitFieldResponse(BaseModel):
    uuid: UUID
    season: UUID
    name: str
    field_type: str
    options: list[Any]
    order: int
    organization: UUID | None
    created_at: datetime

class CreatePitFieldRequest(BaseModel):
    season_uuid: UUID
    name: str
    field_type: str
    options: str
    order: int
    organization_uuid: UUID

class EditPitFieldRequest(CreatePitFieldRequest):
    field_uuid: UUID

class DeletePitFieldRequest(BaseModel):
    field_uuid: UUID

class GetPitsForSeasonRequest(BaseModel):
    season_uuid: UUID
    event_code: str
    event_name: str
    event_type: str
    event_city: str
    event_country: str
    event_start_date: str
    event_end_date: str

class SubmitPitFieldAnswerRequest(BaseModel):
    season_uuid: UUID
    team_number: int
    
    event_code: str
    event_name: str
    event_type: str
    event_city: str
    event_country: str
    event_start_date: str
    event_end_date: str

    answers: dict[Any, Any]
    nickname: str
