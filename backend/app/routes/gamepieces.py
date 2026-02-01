from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import require_superuser
from ..models import GamePiece, Season, User
from ..schemas.generic import MessageResponse
from ..schemas.gamepieces import GamepieceResponse, GamepieceRequest
from ..utils import get_season


router: APIRouter = APIRouter(
    tags=["Gamepieces"],
)

@router.get("/gamepieces", response_model=list[GamepieceResponse])
async def get_gamepieces() -> list[GamepieceResponse]:
    """
    Get all game pieces on the server

    Returns:
        list[GamepieceResponse]: A list of all game pieces
    """
    gamepieces: list[GamePiece] = await GamePiece.all()
    return [
        GamepieceResponse(
            uuid=gp.uuid,
            season=gp.season.uuid,
            name=gp.name,
            created_at=gp.created_at,
        )
        for gp in gamepieces
    ]

@router.post("/gamepieces/create", response_model=GamepieceResponse)
async def create_gamepiece(data: GamepieceRequest, superuser: User = Depends(require_superuser)) -> GamePiece:
    """
    Create a new game piece

    Requires superuser access

    Parameters:
        data (GamepieceRequest): The data to create the game piece

    Returns:
        `GamepieceResponse`: The created game piece
    """
    season: Season = await get_season(data.season_uuid)
    gamepiece: GamePiece = await GamePiece.create(season=season, name=data.name)
    return gamepiece

@router.get("/gamepieces/season/{season_uuid}", response_model=list[GamepieceResponse])
async def get_season_gamepieces(season_uuid: UUID) -> list[GamepieceResponse]:
    """
    Get all game pieces for a season

    Parameters:
        season_uuid (`UUID`): The UUID of the season to get game pieces for

    Returns:
        list[GamepieceResponse]: A list of all game pieces for the season
    """
    season: Season = await get_season(season_uuid)
    gamepieces: list[GamePiece] = await GamePiece.filter(season=season)

    return [
        GamepieceResponse(
            uuid=gp.uuid,
            season=season.uuid,
            name=gp.name,
            created_at=gp.created_at,
        )
        for gp in gamepieces
    ]

@router.delete("/gamepieces/delete/{gamepiece_uuid}", response_model=MessageResponse)
async def delete_gamepiece(gamepiece_uuid: str, superuser: User = Depends(require_superuser)) -> dict[str, str]:
    """
    Delete a game piece

    Requires superuser access

    Parameters:
        gamepiece_uuid (`UUID`): The UUID of the game piece to delete

    Returns:
        `MessageResponse`: A message indicating that the game piece was deleted
    """
    gamepiece: GamePiece | None = await GamePiece.get_or_none(uuid=gamepiece_uuid)
    if not gamepiece:
        raise HTTPException(status_code=404, detail="Game piece not found")
    await gamepiece.delete()
    return {"message": "Game piece deleted"}