from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_current_user
from ..models import GamePiece, Season, User
from ..schemas.generic import MessageResponse
from ..schemas.gamepieces import GamepieceResponse, GamepieceRequest


router: APIRouter = APIRouter(
    tags=["Gamepieces"],
)

@router.get("/gamepieces", response_model=list[GamepieceResponse])
async def get_gamepieces() -> list[GamePiece]:
    gamepieces: list[GamePiece] = await GamePiece.all()
    return gamepieces

@router.post("/gamepieces/create", response_model=GamepieceResponse)
async def create_gamepiece(data: GamepieceRequest, current_user: User = Depends(get_current_user)):
    season: Season | None = await Season.get_or_none(uuid=data.season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    gamepiece: GamePiece = await GamePiece.create(season=season, name=data.name)
    return gamepiece

@router.get("/gamepieces/season/{season_uuid}", response_model=list[GamepieceResponse])
async def get_season_gamepieces(season_uuid: str) -> list[GamePiece]:
    season: Season | None = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    gamepieces: list[GamePiece] = await GamePiece.filter(season=season)
    return gamepieces

@router.delete("/gamepieces/delete/{gamepiece_uuid}", response_model=MessageResponse)
async def delete_gamepiece(gamepiece_uuid: str, current_user: User = Depends(get_current_user)) -> dict[str, str]:
    gamepiece: GamePiece | None = await GamePiece.get_or_none(uuid=gamepiece_uuid)
    if not gamepiece:
        raise HTTPException(status_code=404, detail="Game piece not found")
    await gamepiece.delete()
    return {"message": "Game piece deleted"}