from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

type MyDataTypes = Literal["match_scouting_submission", "match_scouting_answer", "team_pit", "pit_scouting_answer", "event"]

class MyDataResponse(BaseModel):
    uuid: UUID
    type: MyDataTypes
    name: str
    created_at: datetime