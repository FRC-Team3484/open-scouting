from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class OrganizationRequest(BaseModel):
    name: str
    description: str

class OrganizationResponse(BaseModel):
    uuid: str
    name: str
    description: str
    created_at: datetime

class OrganizationMemberResponse(BaseModel):
    uuid: str
    organization: UUID
    user: UUID
    role: str
    created_at: datetime