from fastapi import APIRouter, Form, HTTPException

from ..models import Event, Season


router: APIRouter = APIRouter()

@router.get("/event/custom/{season_uuid}")
async def get_custom_events(season_uuid: str):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    return await Event.filter(season=season, custom=True)

@router.post("/event/custom/{season_uuid}/create")
async def create_custom_event(
    season_uuid: str,

    event_code: str = Form(...),
    event_name: str = Form(...),
    event_type: str = Form(...),
    event_city: str = Form(...),
    event_country: str = Form(...),
    event_start_date: str = Form(...),
    event_end_date: str = Form(...)
    
    ):
    
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    event, _ = await Event.get_or_create(
        season=season,
        event_code=event_code,
        name=event_name,
        type=event_type,
        city=event_city,
        country=event_country,
        start_date=event_start_date,
        end_date=event_end_date,
        custom=True
    )

    return event