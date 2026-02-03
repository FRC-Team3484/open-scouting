from typing import Any
from uuid import UUID

from pydantic import BaseModel, RootModel


class MatchScoutingFieldResponse(BaseModel):
    uuid: UUID | None = None
    name: str
    field_type: str
    stat_type: str
    game_piece_id: UUID | None = None
    required: bool
    options: list[Any] | None = None
    order: int
    organization_id: UUID | None = None

class MatchScoutingFieldRequest(BaseModel):
    name: str
    season_uuid: UUID
    field_type: str
    stat_type: str
    required: bool
    order: int
    organization_uuid: UUID | None = None
    parent_uuid: UUID | None = None
    
    options: list[Any] | None = None
    game_piece_uuid: UUID | None = None

class MatchScoutingFieldRequestUUID(MatchScoutingFieldRequest):
    field_uuid: UUID