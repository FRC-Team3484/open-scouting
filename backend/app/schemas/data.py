

from typing import Any

from pydantic import BaseModel

# /data/filters
class DataFiltersEvent(BaseModel):
    event_code: str
    event_name: str

class DataFiltersTeam(BaseModel):
    team_number: int

class DataFiltersResponse(BaseModel):
    events: list[DataFiltersEvent]
    teams: list[DataFiltersTeam]

# /data/get
class DataMatchValue(BaseModel):
    match_number: int
    value: Any

class DataPercentageValue(BaseModel):
    value: Any
    percentage: float

class DataStatEntry(BaseModel):
    field_uuid: str
    field_type: str
    field_name: str

class DataNumericStatEntry(DataStatEntry):
    values: list[DataMatchValue]
    min: float
    max: float
    avg: float

class DataCapabilityStatEntry(DataStatEntry):
    values: list[Any]
    percentages: list[DataPercentageValue]

class DataOtherStatEntry(DataStatEntry):
    values: list[DataMatchValue]

class DataSummaryEntry(BaseModel):
    field_uuid: str
    field_name: str
    stat_type: str
    avg: float | str
    values: Any

class DataTeamStats(BaseModel):
    Fuel: list[DataNumericStatEntry] = []

class DataTeamResponse(BaseModel):
    team_number: int
    nickname: str | None

    teleop: dict[str, list[DataNumericStatEntry]]
    auton: dict[str, list[DataNumericStatEntry]]

    capability: list[DataCapabilityStatEntry]
    other: list[DataOtherStatEntry]
    summary: list[DataSummaryEntry]