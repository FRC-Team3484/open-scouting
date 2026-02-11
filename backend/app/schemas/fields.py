from random import choices
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, RootModel

class MatchScoutingFieldOptions(BaseModel):
    choices: list[Any]
    default: float
    minimum: float
    maximum: float


class MatchScoutingFieldResponse(BaseModel):
    uuid: UUID | None = None
    name: str
    field_type: str
    stat_type: str
    game_piece_uuid: UUID | None = None
    required: bool
    options: MatchScoutingFieldOptions
    choices: list[Any] = Field(default_factory=list)
    order: int
    organization_id: UUID | None = None

class MatchScoutingFieldRequest(BaseModel):
    uuid: UUID | None = None
    name: str
    season_uuid: UUID
    field_type: str
    stat_type: str
    required: bool
    order: int
    organization_uuid: UUID | None = None
    parent_uuid: UUID | None = None
    
    options: MatchScoutingFieldOptions
    choices: list[Any] = Field(default_factory=list)
    game_piece_uuid: UUID | None = None

class MatchScoutingFieldRequestUUID(MatchScoutingFieldRequest):
    field_uuid: UUID