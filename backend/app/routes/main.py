from fastapi import APIRouter, Depends
from datetime import datetime

from ..dependencies import get_identity
from ..routes.notifications import send_notification

from ..models import Event, MatchScoutingSubmission, Season, TeamPit
from ..schemas.main import ServerStatsResponse, ServerStatusResponse
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

@router.get("/status/stats")
async def get_server_stats(identity = Depends(get_identity)) -> ServerStatsResponse:
    """
    Get basic server stats, which are displayed on the index page
    """
    seasons = await Season.all()
    events_scouted = await Event.all()
    match_scouting_submissions = await MatchScoutingSubmission.all()
    pits_scouted = await TeamPit.filter(answers__isnull=False).distinct()

    # TODO: Remove
    await send_notification(identity.user, "Server stats update", "test notification" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "info")

    return ServerStatsResponse(
        seasons=len(seasons),
        events_scouted=len(events_scouted),
        match_scouting_submissions=len(match_scouting_submissions),
        pits_scouted=len(pits_scouted),
    )