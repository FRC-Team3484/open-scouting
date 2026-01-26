from datetime import datetime

from pydantic import BaseModel


class OrganizationRequest(BaseModel):
    name: str
    description: str

class OrganizationResponse(BaseModel):
    uuid: str
    name: str
    description: str
    created_at: datetime

class MessageResponse(BaseModel):
    message: str

class OrganizationUuidRequest(BaseModel):
    organization_uuid: str

class OrganizationMemberResponse(BaseModel):
    uuid: str
    organization: str
    user: str
    role: str
    created_at: datetime