from typing import Any, Iterator
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
    description: str | None
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
    description: str | None
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

class ReorderMatchScoutingField(BaseModel):
    uuid: UUID
    order: int
    parent_uuid: UUID | None

class ReorderMatchScoutingFieldsRequest(RootModel[list[ReorderMatchScoutingField]]):
    root: list[ReorderMatchScoutingField]

    def __iter__(self) -> Iterator[ReorderMatchScoutingField]:
        return iter(self.root)