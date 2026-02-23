from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from ..utils import IS_DEV
from ..dependencies import get_current_user, require_user
from ..models import Organization, OrganizationMember, User
from ..schemas.generic import MessageResponse
from ..schemas.organizations import OrganizationMemberResponse, OrganizationRequest, OrganizationResponse


router: APIRouter = APIRouter(
    tags=["Organizations"],
    dependencies=[Depends(require_user)],
    include_in_schema=IS_DEV
)

@router.post("/organization/create", response_model=OrganizationResponse)
async def create_organization(data: OrganizationRequest, current_user: User = Depends(get_current_user)) -> Organization:
    """
    Create a new organization

    Parameters:
        data (OrganizationRequest): The data to create the organization

    Returns:
        `Organization`: The created organization
    """
    organization = await Organization.create(name=data.name, description=data.description)
    await OrganizationMember.create(organization=organization, user=current_user, role="admin")
    return organization

@router.get("/organization/all/list", response_model=list[OrganizationResponse])
async def get_organizations() -> list[OrganizationResponse]:
    """
    Get all organizations on the server

    Returns:
        list[Organization]: A list of all organizations
    """
    organizations: list[Organization] = await Organization.all()
    return [
        OrganizationResponse(
            uuid=organization.uuid,
            name=organization.name,
            description=organization.description,
            created_at=organization.created_at,
        )
        for organization in organizations
    ]

@router.get("/organization/me/list", response_model=list[OrganizationResponse])
async def get_user_organizations(current_user: User = Depends(get_current_user)) -> list[OrganizationResponse]:
    """
    Get all organizations that the current user is a member of

    Returns:
        list[Organization]: A list of all organizations
    """
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    organization_members: list[OrganizationMember] = await OrganizationMember.filter(user=user)
    organizations: list[Organization] = await Organization.filter(uuid__in=[m.organization_id for m in organization_members])

    return [
        OrganizationResponse(
            uuid=organization.uuid,
            name=organization.name,
            description=organization.description,
            created_at=organization.created_at,
        )
        for organization in organizations
    ]

@router.get("/organization/{organization_uuid}", response_model=OrganizationResponse)
async def get_organization(organization_uuid: UUID) -> Organization:
    """
    Get a specific organization

    Parameters:
        data (OrganizationUuidRequest): The data to get the organization

    Returns:
        `Organization`: The organization
    """
    organization: Organization | None = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.delete("/organization/delete/{organization_uuid}", response_model=MessageResponse)
async def delete_organization(organization_uuid: UUID, current_user: User = Depends(get_current_user)) -> dict[str, str]:
    """
    Delete a specific organization

    Parameters:
        data (OrganizationUuidRequest): The data to delete the organization

    Returns:
        `MessageResponse`: A message indicating that the organization was deleted
    """
    # TODO: Only be able to delete organizations that the user is an admin of
    organization: Organization | None = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    await organization.delete()
    return {"message": "Organization deleted"}

@router.get("/organization/{organization_uuid}/members", response_model=list[OrganizationMemberResponse])
async def get_organization_members(organization_uuid: UUID) -> list[OrganizationMemberResponse]:
    """
    Get all members of a specific organization

    Parameters:
        data (OrganizationUuidRequest): The data to get the organization members

    Returns:
        list[OrganizationMember]: A list of all organization members
    """
    organization: Organization | None = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    members: list[OrganizationMember] = await OrganizationMember.filter(organization=organization)
    
    return [
        OrganizationMemberResponse(
            uuid=member.uuid,
            organization=member.organization_id,
            user=member.user_id,
            role=member.role,
            created_at=member.created_at,
        )
        for member in members
    ]