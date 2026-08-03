

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

# Create report
class CreateReportRequest(BaseModel):
    type: Literal["match_scouting_submission", "match_scouting_answer", "team_pit", "pit_scouting_answer", "event"]
    content_uuid: UUID
    report_reason: Literal["spam", "innaccurate", "inappropriate", "offensive", "duplicate", "other"]
    report_details: str

class CreateReportResponse(CreateReportRequest):
    uuid: UUID

# Get reports
class MatchScoutingAnswerReportDetails(BaseModel):
    uuid: UUID
    field_uuid: UUID
    value: str
    created_at: datetime | None = None

class MatchScoutingSubmissionReportDetails(BaseModel):
    uuid: UUID
    event_uuid: UUID
    season_uuid: UUID
    team_number: int
    match_number: int
    match_type: str
    answers_count: int
    answers: list[MatchScoutingAnswerReportDetails]

class TeamPitReportDetails(BaseModel):
    uuid: UUID
    team_number: int
    nickname: str
    season_uuid: UUID
    event_uuid: UUID

class PitScoutingAnswerReportDetails(BaseModel):
    uuid: UUID
    field_uuid: UUID
    value: str
    team_uuid: UUID
    team_number: int
    created_at: datetime

class EventReportDetails(BaseModel):
    uuid: UUID
    season_uuid: UUID
    event_code: str
    name: str
    type: str
    city: str
    country: str
    start_date: datetime
    end_date: datetime
    custom: bool
    created_at: datetime

class ReportResponse(BaseModel):
    uuid: UUID
    type: Literal["match_scouting_submission", "match_scouting_answer", "team_pit", "pit_scouting_answer", "event"]
    content_uuid: UUID
    content_details: MatchScoutingSubmissionReportDetails | MatchScoutingAnswerReportDetails | TeamPitReportDetails | PitScoutingAnswerReportDetails | EventReportDetails | None
    report_reason: Literal["spam", "innaccurate", "inappropriate", "offensive", "duplicate", "other"]
    report_details: str
    created_at: datetime