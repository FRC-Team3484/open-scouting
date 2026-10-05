
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class MatchScoutingFieldType:
    """
    Compat dataclass for removed MatchScoutingField from models.py (removed in favor of ScoutingField in v2.3.0)

    This is used to preserve a degree of type hinting in the custom migrations 0019 and 0021
    """
    uuid: UUID
    parent: Any
    season: Any
    name: str
    description: str
    field_type: str
    stat_type: str
    game_piece: Any
    required: bool
    options: Any
    order: int
    organization: Any
    archived: bool
    created_at: datetime
    created_by: Any

@dataclass
class PitScoutingFieldType:
    """
    Compat dataclass for removed PitScoutingField from models.py (removed in favor of ScoutingField in v2.3.0)

    This is used to preserve a degree of type hinting in the custom migrations 0019 and 0021
    """
    uuid: UUID
    season: Any
    name: str
    description: str
    required: bool
    field_type: str
    options: Any
    order: int
    organization: Any
    archived: bool
    created_at: datetime
    created_by: Any