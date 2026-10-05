from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field, RootModel

# Repair response
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

class ScoutingFieldRepair(BaseRepair):
    data_type: Literal["scouting_field"]
    repair_type: Literal["missing_season", "missing_game_piece", "missing_season"]

class MatchScoutingSubmissionRepair(BaseRepair):
    data_type: Literal["match_scouting_submission"]
    repair_type: Literal["missing_event"]

class MatchScoutingAnswerRepair(BaseRepair):
    data_type: Literal["match_scouting_answer"]
    repair_type: Literal["missing_field","missing_submission"]

class TeamPitRepair(BaseRepair):
    data_type: Literal["team_pit"]
    repair_type: Literal["missing_season", "missing_event"]

class PitScoutingAnswerRepair(BaseRepair):
    data_type: Literal["pit_scouting_answer"]
    repair_type: Literal["missing_field", "missing_team"]

Repair = Annotated[
    EventRepair | 
    GamePieceRepair | 
    ScoutingFieldRepair | 
    MatchScoutingSubmissionRepair | 
    MatchScoutingAnswerRepair | 
    TeamPitRepair | 
    PitScoutingAnswerRepair,
    Field(discriminator="data_type")
]

class RepairResponse(RootModel[Repair]):
    pass

# Avaliable data that can be used for repairs
class ScoutingFieldRepairResponse(BaseModel):
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

# Repair request
class BaseRepairRequest(BaseModel):
    data_uuid: UUID # UUID of the data that needs to be fixed
    content_uuid: UUID | None = None # UUID of the content to fix the issue. None when repair_type is "missing_event"

class EventRepairRequest(BaseRepairRequest):
    data_type: Literal["event"]
    repair_type: Literal["missing_season"]

class GamePieceRepairRequest(BaseRepairRequest):
    data_type: Literal["game_piece"]
    repair_type: Literal["missing_season"]

class ScoutingFieldRepairRequest(BaseRepairRequest):
    data_type: Literal["scouting_field"]
    repair_type: Literal["missing_season", "missing_game_piece"]

class MatchScoutingSubmissionRepairRequest(BaseRepairRequest):
    data_type: Literal["match_scouting_submission"]
    repair_type: Literal["missing_event"]
    event_code: str | None = None # Used when repair_type is "missing_event"

class MatchScoutingAnswerRepairRequest(BaseRepairRequest):
    data_type: Literal["match_scouting_answer"]
    repair_type: Literal["missing_field","missing_submission"]

class TeamPitRepairRequest(BaseRepairRequest):
    data_type: Literal["team_pit"]
    repair_type: Literal["missing_season", "missing_event"]
    event_code: str | None = None # Used when repair_type is "missing_event"

class PitScoutingAnswerRepairRequest(BaseRepairRequest):
    data_type: Literal["pit_scouting_answer"]
    repair_type: Literal["missing_field", "missing_team"]

RepairRequest = Annotated[
    EventRepairRequest | 
    GamePieceRepairRequest | 
    ScoutingFieldRepairRequest | 
    MatchScoutingSubmissionRepairRequest | 
    MatchScoutingAnswerRepairRequest | 
    TeamPitRepairRequest | 
    PitScoutingAnswerRepairRequest,
    Field(discriminator="data_type")
]