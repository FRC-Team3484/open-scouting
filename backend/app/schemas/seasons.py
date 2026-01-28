from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class SeasonBase(BaseModel):
    year: int
    name: str
    active: bool

class SeasonCreate(SeasonBase):
    pass

class SeasonResponse(SeasonBase):
    uuid: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }