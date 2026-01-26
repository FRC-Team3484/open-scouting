from datetime import datetime
import uuid
from pydantic import BaseModel


class GamepieceResponse(BaseModel):
    uuid: uuid.UUID
    season: uuid.UUID
    name: str
    created_at: datetime

class GamepieceRequest(BaseModel):
    season_uuid: uuid.UUID
    name: str

class MessageResponse(BaseModel):
    message: str