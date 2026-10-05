from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, JsonValue

from ..models import FieldType, ScoutingType, StatType


class FieldChoiceResponse(BaseModel):
    uuid: UUID
    name: str
    simple_name: str
    created_at: datetime

class FieldOptionsResponse(BaseModel):
    uuid: UUID
    choices: list[FieldChoiceResponse] | None
    default: int | None
    minimum: int | None
    maximum: int | None
    created_at: datetime

class MatchScoutingField(BaseModel):
    uuid: UUID
    season_uuid: UUID | None
    organization_uuid: UUID | None
    parent_uuid: UUID | None
    name: str
    description: str | None
    scouting_type: Literal[ScoutingType.MATCH]
    field_type: FieldType
    stat_type: StatType | None
    game_piece_uuid: UUID | None
    required: bool
    options: FieldOptionsResponse | None
    order: int
    archived: bool
    created_at: datetime

class MatchScoutingFieldResponse(MatchScoutingField):
    created_at: datetime

class MatchScoutingFieldRequest(MatchScoutingField):
    pass

class PitScoutingField(BaseModel):
    uuid: UUID
    season_uuid: UUID | None
    organization_uuid: UUID | None
    name: str
    description: str | None
    scouting_type: Literal[ScoutingType.PIT]
    field_type: FieldType
    required: bool
    options: FieldOptionsResponse | None
    order: int
    archived: bool

class PitScoutingFieldResponse(PitScoutingField):
    created_at: datetime

class PitScoutingFieldRequest(PitScoutingField):
    pass

class ScoutingFieldPresetResponse(BaseModel):
    name: str
    preset: JsonValue