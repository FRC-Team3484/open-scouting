from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from ..utils import IS_DEV
from ..dependencies import require_superuser
from ..models import Season, User
from ..schemas.generic import MessageResponse
from ..schemas.seasons import SeasonCreate, SeasonResponse


router: APIRouter = APIRouter(
    tags=["Seasons"],
    include_in_schema=IS_DEV
)

@router.get("/seasons", response_model=list[SeasonResponse])
async def get_seasons() -> list[Season]:
    """
    Get all seasons on the server

    Returns:
        list[Season]: A list of all seasons
    """
    return await Season.all()

@router.get("/seasons/active", response_model=SeasonResponse | None)
async def get_active_season() -> Season | None:
    """
    Get the active season on the server

    Returns:
        Season: The active season
    """
    return await Season.get_or_none(active=True)

@router.post("/seasons/create", response_model=SeasonResponse)
async def create_season(
        data: SeasonCreate,
        superuser: User = Depends(require_superuser),
    ) -> Season:
    """
    Create a new season

    Requires superuser access

    Parameters:
        data (`SeasonCreate`): The data to create the season

    Returns:
        `SeasonResponse`: The created season
    """

    return await Season.create(**data.model_dump())

@router.delete("/seasons/delete/{season_uuid}", response_model=MessageResponse)
async def delete_season(
        season_uuid: str,
        superuser: User = Depends(require_superuser),
    ) -> dict[str, str]:
    """
    Delete a season

    Requires superuser access

    Parameters:
        season_uuid (`UUID`): The UUID of the season to delete

    Returns:
        `MessageResponse`: A message indicating that the season was deleted
    """

    season: Season | None = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    await season.delete()
    return {"message": "Season deleted"}

@router.post("/seasons/activate/{season_uuid}", response_model=MessageResponse)
async def activate_season(season_uuid: UUID, superuser = Depends(require_superuser)):
    """
    Deactivate the current season and make the given season active

    Requires superuser access

    Paramaters:
        season_uuid (`UUID`): The UUID of the season to activate

    Returns:
        `MessageResponse`: A message indicating that the season was made active
    """

    active_season = await Season.get_or_none(active=True)

    if active_season:
        active_season.active = False
        await active_season.save()

    new_season = await Season.get_or_none(uuid=season_uuid)

    if not new_season:
        raise HTTPException(status_code=404, detail="Season not found")

    new_season.active = True
    await new_season.save()

    return {"message": "Season activated"}