from fastapi import APIRouter, Depends, Form, HTTPException

from ..dependencies import get_current_user
from ..models import Organization, OrganizationMember, User


router: APIRouter = APIRouter()

@router.post("/organization/create")
async def create_organization(name: str = Form(...), description: str = Form(...), current_user: User = Depends(get_current_user)):
    organization = await Organization.create(name=name, description=description)
    await OrganizationMember.create(organization=organization, user=current_user, role="admin")
    return organization

@router.get("/organization/all/list")
async def get_organizations():
    organizations = await Organization.all()
    return organizations

@router.get("/organization/me/list")
async def get_user_organizations(current_user: User = Depends(get_current_user)):
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    organization_members = await OrganizationMember.filter(user=user)
    organizations = await Organization.filter(uuid__in=[m.organization_id for m in organization_members])

    return organizations

@router.get("/organization/{organization_uuid}")
async def get_organization(organization_uuid: str):
    organization = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.delete("/organization/delete/{organization_uuid}")
async def delete_organization(organization_uuid: str, current_user: User = Depends(get_current_user)):
    organization = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    await organization.delete()
    return {"message": "Organization deleted"}

@router.get("/organization/{organization_uuid}/members")
async def get_organization_members(organization_uuid: str, current_user: User = Depends(get_current_user)):
    organization = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    members = await OrganizationMember.filter(organization=organization)
    return members