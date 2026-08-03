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
    value: str | bool | int | float | None

class DataPercentageValue(BaseModel):
    value: str | bool | int | float | None
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
    values: list[str | bool | int | float | None]
    percentages: list[DataPercentageValue]

class DataOtherStatEntry(DataStatEntry):
    values: list[DataMatchValue]

class DataSummaryEntry(BaseModel):
    field_uuid: str
    field_name: str
    stat_type: str
    avg: float | str
    values: list[int | float] | dict[str | bool, float] # If list, it's a score or miss field with values. If dict, it's key value pairs for a capability field

class DataTeamStats(BaseModel):
    Fuel: list[DataNumericStatEntry] = []

class DataTeamResponse(BaseModel):
    team_number: int
    nickname: str | None

    # Key is game piece, value is data for each field
    teleop: dict[str, list[DataNumericStatEntry]]
    auton: dict[str, list[DataNumericStatEntry]]

    capability: list[DataCapabilityStatEntry]
    other: list[DataOtherStatEntry]
    summary: list[DataSummaryEntry]