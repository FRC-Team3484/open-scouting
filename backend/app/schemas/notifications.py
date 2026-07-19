
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    uuid: UUID
    title: str
    message: str
    type: str
    action_type: str | None
    action_data: dict[Any, Any] | None
    read: bool
    created_at: datetime

class NotificationRequest(BaseModel):
    uuid: UUID
    title: str
    message: str
    type: str
    action_type: str | None
    action_data: dict[Any, Any] | None
    read: bool
    deleted: bool