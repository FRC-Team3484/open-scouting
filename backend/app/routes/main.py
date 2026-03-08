from fastapi import APIRouter

from ..models import Season
from ..schemas.main import ServerStatusResponse
from ..constants import VERSION


router: APIRouter = APIRouter(
    tags=["Generic"],
)

@router.get("/status")
async def get_server_status() -> ServerStatusResponse:
    active_season = await Season.get_or_none(active=True)

    return ServerStatusResponse(
        version=VERSION,
        active_season=active_season.uuid,
    )