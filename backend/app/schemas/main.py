import uuid
from pydantic import BaseModel

class ServerStatusResponse(BaseModel):
    version: str | None
    active_season: uuid.UUID