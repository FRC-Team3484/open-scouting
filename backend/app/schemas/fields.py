from typing import Any
from uuid import UUID

from pydantic import BaseModel, RootModel


class MatchScoutingField(BaseModel):
    uuid: UUID | None
    name: str
    field_type: str
    stat_type: str
    game_piece_id: UUID | None
    required: bool
    options: list[Any]
    order: int
    organization_id: UUID | None
    fields: list[MatchScoutingField]

class MatchScoutingFieldsResponse(RootModel[list[MatchScoutingField]]):
    root: list[MatchScoutingField]

class MatchScoutingFieldRequest(MatchScoutingField):
    season_uuid: UUID
    organization_uuid: UUID
    game_piece_uuid: UUID
    parent_uuid: UUID | None
    field_uuid: UUID | None

class MatchScoutingFieldRequestUUID(MatchScoutingFieldRequest):
    field_uuid: UUID