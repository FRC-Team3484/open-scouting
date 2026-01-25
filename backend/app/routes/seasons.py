from fastapi import APIRouter, Depends, Form, HTTPException

from ..dependencies import get_current_user
from ..models import Season, User


router: APIRouter = APIRouter()

@router.get("/seasons")
async def get_seasons():
    seasons = await Season.all()
    return seasons

@router.get("/seasons/active")
async def get_active_season():
    season = await Season.get_or_none(active=True)
    return season

@router.post("/seasons/create")
async def create_season(year: int = Form(...), name: str = Form(...), active: bool = Form(...), current_user: User = Depends(get_current_user)):
    season = await Season.create(year=year, name=name, active=active)
    return season

@router.delete("/seasons/delete/{season_uuid}")
async def delete_season(season_uuid: str, current_user: User = Depends(get_current_user)):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    await season.delete()
    return {"message": "Season deleted"}