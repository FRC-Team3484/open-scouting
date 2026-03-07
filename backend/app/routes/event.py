from collections import defaultdict
from uuid import UUID
from fastapi import APIRouter, Depends

from ..schemas.generic import MessageResponse
from ..models import Event, MatchScoutingSubmission, Season, TeamPit
from ..schemas.event import AdminEventResponse, EventResponse, CustomEventRequest
from ..utils import get_season, IS_DEV
from ..dependencies import require_superuser

router: APIRouter = APIRouter(
    tags=["Events"],
    include_in_schema=IS_DEV
)

@router.get("/event/custom/{season_uuid}", response_model=list[EventResponse])
async def get_custom_events(season_uuid: str) -> list[EventResponse]:
    """
    Get all custom events for a season

    Parameters:
        season_uuid (`UUID`): The UUID of the season to get custom events for

    Returns:
        list[EventResponse]: A list of all custom events for the season
    """
    season: Season = await get_season(season_uuid)

    return [
        EventResponse(
            uuid=event.uuid,
            season=season.uuid,
            event_code=event.event_code,
            name=event.name,
            type=event.type,
            city=event.city,
            country=event.country,
            start_date=event.start_date,
            end_date=event.end_date,
            pits_generated=event.pits_generated,
            custom=event.custom,
            created_at=event.created_at
        ) for event in await Event.filter(season=season, custom=True)
    ]

@router.post("/event/custom/{season_uuid}/create", response_model=EventResponse)
async def create_custom_event(
        season_uuid: UUID,
        data: CustomEventRequest
    ) -> EventResponse:
    """
    Create a custom event for a season

    Parameters:
        season_uuid (`UUID`): The UUID of the season to create a custom event for
        data (`CustomEventRequest`): The UUID of the season to create a custom event for

    Returns:
        EventResponse: The created custom event
    """
    
    season: Season = await get_season(season_uuid)

    event, _ = await Event.get_or_create(
        season=season,
        event_code=data.event_code,
        name=data.event_name,
        type=data.event_type,
        city=data.event_city,
        country=data.event_country,
        start_date=data.event_start_date,
        end_date=data.event_end_date,
        custom=True
    )

    return EventResponse(
        uuid=event.uuid,
        season=season.uuid,
        event_code=event.event_code,
        name=event.name,
        type=event.type,
        city=event.city,
        country=event.country,
        start_date=event.start_date,
        end_date=event.end_date,
        pits_generated=event.pits_generated,
        custom=event.custom,
        created_at=event.created_at
    )

@router.get("/events/get", response_model=list[AdminEventResponse])
async def get_all_events(superuser = Depends(require_superuser)) -> list[AdminEventResponse]:
    """
    Get all events on the server, used for the admin dashboard

    Requires superuser access

    Returns:
        list[EventResponse]: A list of all events
    """
    
    match_counts = defaultdict(int)
    pit_counts = defaultdict(int)

    for row in await MatchScoutingSubmission.all().values("event_id"):
        match_counts[row["event_id"]] += 1

    for row in await TeamPit.all().values("event_id"):
        pit_counts[row["event_id"]] += 1

    events = [
        AdminEventResponse(
            uuid=event.uuid,
            season=event.season.uuid,
            event_code=event.event_code,
            name=event.name,
            type=event.type,
            city=event.city,
            country=event.country,
            start_date=event.start_date,
            end_date=event.end_date,
            pits_generated=event.pits_generated,
            custom=event.custom,
            created_at=event.created_at,
            match_scouting_submissions=match_counts[event.uuid],
            pits=pit_counts[event.uuid]
        ) for event in await Event.all().select_related("season")
    ]

    return events

@router.delete("/events/delete/{event_uuid}", response_model=MessageResponse)
async def delete_event(event_uuid: UUID, superuser = Depends(require_superuser)) -> MessageResponse:
    """
    Delete an event

    Requires superuser access

    Parameters:
        event_uuid (`UUID`): The UUID of the event to delete

    Returns:
        MessageResponse: A message indicating that the event was deleted
    """
    await Event.filter(uuid=event_uuid).delete()
    return MessageResponse(message="Event deleted")

@router.delete("/events/delete/{event_uuid}/match_scouting_submissions", response_model=MessageResponse)
async def delete_match_scouting_submissions(event_uuid: UUID, superuser = Depends(require_superuser)) -> MessageResponse:
    """
    Delete all match scouting submissions for an event

    Requires superuser access

    Parameters:
        event_uuid (`UUID`): The UUID of the event to delete match scouting submissions for

    Returns:
        MessageResponse: A message indicating that the match scouting submissions were deleted
    """
    await MatchScoutingSubmission.filter(event_id=event_uuid).delete()
    return MessageResponse(message="Match scouting submissions deleted")

@router.delete("/events/delete/{event_uuid}/team_pits", response_model=MessageResponse)
async def delete_team_pits(event_uuid: UUID, superuser = Depends(require_superuser)) -> MessageResponse:
    """
    Delete all team pits for an event

    Requires superuser access

    Parameters:
        event_uuid (`UUID`): The UUID of the event to delete team pits for

    Returns:
        MessageResponse: A message indicating that the team pits were deleted
    """
    await TeamPit.filter(event_id=event_uuid).delete()
    await Event.filter(uuid=event_uuid).update(pits_generated=False)
    
    return MessageResponse(message="Team pits deleted")