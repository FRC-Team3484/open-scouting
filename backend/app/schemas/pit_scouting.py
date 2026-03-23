from datetime import datetime
from typing import Any, Iterator
from uuid import UUID

from pydantic import BaseModel, RootModel


class PitFieldsRequest(BaseModel):
    season_uuid: UUID

class PitFieldOptions(BaseModel):
    choices: list[Any]

class PitFieldResponse(BaseModel):
    uuid: UUID
    season: UUID
    name: str
    description: str | None
    required: bool
    field_type: str
    options: PitFieldOptions
    order: int
    organization: UUID | None
    created_at: datetime

class PitFieldRequest(BaseModel):
    season_uuid: UUID
    name: str
    description: str | None
    required: bool
    field_type: str
    options: PitFieldOptions
    order: int
    organization_uuid: UUID | None = None

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
    event_custom: bool

class SubmitPitFieldAnswerRequest(BaseModel):
    uuid: UUID
    season_uuid: UUID
    team_number: int
    
    event_code: str
    event_name: str
    event_type: str
    event_city: str
    event_country: str
    event_start_date: str
    event_end_date: str

    answers: list[Any]
    nickname: str

class ReorderPitField(BaseModel):
    uuid: UUID
    order: int

class ReorderPitFieldsRequest(RootModel[list[ReorderPitField]]):
    root: list[ReorderPitField]

    def __iter__(self) -> Iterator[ReorderPitField]:
        return iter(self.root)

class AdminPitResponse(BaseModel):
    uuid: UUID
    event_name: str
    event_code: str
    team_number: int
    answers: int
    created_at: datetime