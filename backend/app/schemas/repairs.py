from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field, RootModel


class BaseRepair(BaseModel):
    name: str
    data_uuid: UUID
    data_created_at: datetime

class EventRepair(BaseRepair):
    data_type: Literal["event"]
    repair_type: Literal["missing_season"]

class GamePieceRepair(BaseRepair):
    data_type: Literal["game_piece"]
    repair_type: Literal["missing_season"]

class MatchScoutingFieldRepair(BaseRepair):
    data_type: Literal["match_scouting_field"]
    repair_type: Literal["missing_season", "missing_game_piece"]

class MatchScoutingSubmissionRepair(BaseRepair):
    data_type: Literal["match_scouting_submission"]
    repair_type: Literal["missing_event"]

class MatchScoutingAnswerRepair(BaseRepair):
    data_type: Literal["match_scouting_answer"]
    repair_type: Literal["missing_field","missing_submission"]

class PitScoutingFieldRepair(BaseRepair):
    data_type: Literal["pit_scouting_field"]
    repair_type: Literal["missing_season"]

class TeamPitRepair(BaseRepair):
    data_type: Literal["team_pit"]
    repair_type: Literal["missing_season", "missing_event"]

class PitScoutingAnswerRepair(BaseRepair):
    data_type: Literal["pit_scouting_answer"]
    repair_type: Literal["missing_field", "missing_team"]

Repair = Annotated[
    EventRepair | 
    GamePieceRepair | 
    MatchScoutingFieldRepair | 
    MatchScoutingSubmissionRepair | 
    MatchScoutingAnswerRepair | 
    PitScoutingFieldRepair | 
    TeamPitRepair | 
    PitScoutingAnswerRepair,
    Field(discriminator="data_type")
]

class RepairResponse(RootModel[Repair]):
    pass

class MatchScoutingFieldRepairResponse(BaseModel):
    uuid: UUID
    name: str
    season_year: int | None
    game_piece_name: str | None
    archived: bool
    created_at: datetime

class PitScoutingFieldRepairResponse(BaseModel):
    uuid: UUID
    name: str
    season_year: int | None
    archived: bool
    created_at: datetime