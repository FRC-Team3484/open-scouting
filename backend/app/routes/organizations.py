from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_current_user, require_user
from ..models import Organization, OrganizationMember, User
from ..schemas.generic import MessageResponse
from ..schemas.organizations import OrganizationMemberResponse, OrganizationUuidRequest, OrganizationRequest, OrganizationResponse


router: APIRouter = APIRouter(
    tags=["Organizations"],
    dependencies=[Depends(require_user)],
)

@router.post("/organization/create", response_model=OrganizationResponse)
async def create_organization(data: OrganizationRequest, current_user: User = Depends(get_current_user)) -> Organization:
    organization = await Organization.create(name=data.name, description=data.description)
    await OrganizationMember.create(organization=organization, user=current_user, role="admin")
    return organization

@router.get("/organization/all/list", response_model=list[OrganizationResponse])
async def get_organizations() -> list[Organization]:
    organizations: list[Organization] = await Organization.all()
    return organizations

@router.get("/organization/me/list", response_model=list[OrganizationResponse])
async def get_user_organizations(current_user: User = Depends(get_current_user)) -> list[Organization]:
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    organization_members: list[OrganizationMember] = await OrganizationMember.filter(user=user)
    organizations: list[Organization] = await Organization.filter(uuid__in=[m.organization_id for m in organization_members])

    return organizations

@router.get("/organization/{organization_uuid}", response_model=OrganizationResponse)
async def get_organization(data: OrganizationUuidRequest) -> Organization:
    organization: Organization | None = await Organization.get_or_none(uuid=data.organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.delete("/organization/delete/{organization_uuid}", response_model=MessageResponse)
async def delete_organization(data: OrganizationUuidRequest) -> dict[str, str]:
    organization: Organization | None = await Organization.get_or_none(uuid=data.organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    await organization.delete()
    return {"message": "Organization deleted"}

@router.get("/organization/{organization_uuid}/members", response_model=list[OrganizationMemberResponse])
async def get_organization_members(data: OrganizationUuidRequest) -> list[OrganizationMember]:
    organization: Organization | None = await Organization.get_or_none(uuid=data.organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    members: list[OrganizationMember] = await OrganizationMember.filter(organization=organization)
    return members