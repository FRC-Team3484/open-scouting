from fastapi import APIRouter, Depends, Form, HTTPException

from ..dependencies import get_current_user
from ..models import GamePiece, Season, User

router: APIRouter = APIRouter()

@router.get("/gamepieces")
async def get_gamepieces():
    gamepieces = await GamePiece.all()
    return gamepieces

@router.post("/gamepieces/create")
async def create_gamepiece(season_uuid: str = Form(...), name: str = Form(...), current_user: User = Depends(get_current_user)):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    gamepiece = await GamePiece.create(season=season, name=name)
    return gamepiece

@router.get("/gamepieces/season/{season_uuid}")
async def get_season_gamepieces(season_uuid: str):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    gamepieces = await GamePiece.filter(season=season)
    return gamepieces

@router.delete("/gamepieces/delete/{gamepiece_uuid}")
async def delete_gamepiece(gamepiece_uuid: str, current_user: User = Depends(get_current_user)):
    gamepiece = await GamePiece.get_or_none(uuid=gamepiece_uuid)
    if not gamepiece:
        raise HTTPException(status_code=404, detail="Game piece not found")
    await gamepiece.delete()
    return {"message": "Game piece deleted"}