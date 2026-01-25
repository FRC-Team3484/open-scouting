import json
import os
import httpx

from fastapi import APIRouter, Depends, Form, HTTPException

from ..dependencies import get_current_user
from ..models import Event, Organization, PitScoutingAnswer, PitScoutingField, Season, TeamPit, User


router: APIRouter = APIRouter()

TBA_API_KEY = os.getenv("TBA_API_KEY")


@router.get("/pits/fields/{season_uuid}")
async def get_pit_fields(season_uuid: str):
    season = await Season.get_or_none(uuid=season_uuid)

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    fields = await PitScoutingField.filter(season=season)
    return fields

@router.delete("/pits/fields/{season_uuid}/clear")
async def clear_pit_fields(season_uuid: str, current_user: User = Depends(get_current_user)):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    await PitScoutingField.filter(season=season).delete()
    return {"message": "Fields cleared"}

@router.post("/pits/fields/{season_uuid}/create")
async def create_pit_field(
    season_uuid: str,

    name: str = Form(...),
    field_type: str = Form(...),
    options: str = Form(...),
    order: int = Form(...),
    organization_uuid: str = Form(...)
    ):

    print(options)

    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    if organization_uuid != "":
        organization = await Organization.get_or_none(uuid=organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    field = await PitScoutingField.create(
        season=season,
        name=name,
        field_type=field_type,
        options=options,
        order=order,
        organization=organization
    )
    return field

@router.patch("/pits/fields/{season_uuid}/edit/{field_uuid}")
async def edit_pit_field(
    season_uuid: str, 
    field_uuid: str,

    name: str = Form(...),
    field_type: str = Form(...),
    options: str = Form(...),
    order: int = Form(...),
    organization_uuid: str = Form(...)
    
    ):
    
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    field = await PitScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    if organization_uuid != "":
        organization = await Organization.get_or_none(uuid=organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    field.name = name
    field.field_type = field_type
    field.options = options
    field.order = order
    field.organization = organization

    await field.save()
    return field

@router.delete("/pits/fields/{field_uuid}/delete")
async def delete_pit_field(
        field_uuid: str, 
        current_user: User = Depends(get_current_user)
    ):

    field = await PitScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    await field.delete()
    return field

@router.post("/pits/get/{season_uuid}")
async def get_pits(
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
        end_date=event_end_date
    )

    # If pits have not been generated yet, get teams from TBA and create TeamPits
    if not event.pits_generated and TBA_API_KEY != "" and TBA_API_KEY is not None and event.custom is False:
        event_key = str(season.year) + event_code
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"https://www.thebluealliance.com/api/v3/event/{event_key}/teams",
                headers={"X-TBA-Auth-Key": TBA_API_KEY},
            )

        teams = response.json()

        for team in teams:
            _ = await TeamPit.create(
                team_number=team["team_number"],
                nickname=team["nickname"],
                season=season,
                event=event
            )

        event.pits_generated = True
        await event.save()

    pits = await TeamPit.filter(event=event).prefetch_related("answers")
    return [
        {
            "uuid": pit.uuid,
            "team_number": pit.team_number,
            "nickname": pit.nickname,
            "created_at": pit.created_at,
            "answers": [
                {
                    "uuid": ans.uuid,
                    "field_uuid": ans.field_id,
                    "value": ans.value,
                    "username": ans.username,
                    "created_at": ans.created_at
                }
                for ans in pit.answers
            ]
        }
        for pit in pits
    ]

@router.post("/pits/submit/{season_uuid}/{team_number}")
async def submit_pit(
    season_uuid: str, 
    team_number: int,

    event_code: str = Form(...),
    event_name: str = Form(...),
    event_type: str = Form(...),
    event_city: str = Form(...),
    event_country: str = Form(...),
    event_start_date: str = Form(...),
    event_end_date: str = Form(...),

    answers: str = Form(...),
    nickname: str = Form(...)
    ):
    """
    Get the season and event from the uuids. Then, check if a pit with that team number exists.
    If it does, update that pit

    For the answers in that pit, find each answer that does not already exist on the server, and add them

    If a pit does not exist, that means it was created by the client of a user. It should be created.
    """
    
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    event = await Event.get_or_none(event_code=event_code, season=season).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    pit, created = await TeamPit.get_or_create(
        team_number=team_number,
        season=season,
        event=event,
        nickname=nickname
    )

    if created:
        print("Created pit", pit.uuid, "for team", team_number, "and event", event.uuid)

    for answer in json.loads(answers):
        field = await PitScoutingField.get_or_none(uuid=answer["field_uuid"])

        if not field:
            raise HTTPException(status_code=404, detail="Field not found")

        _, created = await PitScoutingAnswer.get_or_create(
            uuid=answer["uuid"],
            team=pit,
            field=field,
            value=answer["value"],
            username=answer["username"]
        )

        if created:
            print("Created answer", answer["uuid"], "for pit", pit.uuid, "and field", field.uuid)

    return