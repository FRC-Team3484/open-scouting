from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class SeasonBase(BaseModel):
    year: int
    name: str
    active: bool

class SeasonCreate(SeasonBase):
    pass

class SeasonOut(SeasonBase):
    uuid: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class MessageOut(BaseModel):
    message: str