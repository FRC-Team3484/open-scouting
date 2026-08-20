from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PasskeyResponse(BaseModel):
    uuid: UUID
    label: str | None
    created_at: datetime