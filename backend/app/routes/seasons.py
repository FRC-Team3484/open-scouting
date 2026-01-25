from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_current_user
from ..models import Season, User
from ..schemas.seasons import MessageOut, SeasonCreate, SeasonOut


router: APIRouter = APIRouter()

@router.get("/seasons", response_model=list[SeasonOut])
async def get_seasons() -> list[Season]:
    return await Season.all()

@router.get("/seasons/active", response_model=SeasonOut | None)
async def get_active_season() -> Season | None:
    return await Season.get_or_none(active=True)

@router.post("/seasons/create", response_model=SeasonOut)
async def create_season(
    data: SeasonCreate,
    current_user: User = Depends(get_current_user),
    ) -> Season:

    return await Season.create(**data.model_dump())

@router.delete("/seasons/delete/{season_uuid}", response_model=MessageOut)
async def delete_season(
    season_uuid: str,
    current_user: User = Depends(get_current_user),
    ) -> dict[str, str]:

    season: Season | None = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    await season.delete()
    return {"message": "Season deleted"}
