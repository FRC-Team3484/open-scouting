import json
from fastapi import APIRouter, Form, HTTPException
from tortoise.exceptions import IntegrityError

from ..models import Event, MatchScoutingAnswer, MatchScoutingField, MatchScoutingSubmission, Season, User


router: APIRouter = APIRouter()

@router.post("/scouting/submit")
async def submit_match_scouting(
    submission_uuid: str = Form(...),
    fields: str = Form(...),
    user_uuid: str = Form(...), # Is either the UUID for the authenticated user, or just a username
    year: int = Form(...),
    team_number: int = Form(...),
    match_number: int = Form(...),
    match_type: str = Form(...),
    event_code: str = Form(...),
    event_name: str = Form(...),
    event_type: str = Form(...),
    event_city: str = Form(...),
    event_country: str = Form(...),
    event_start_date: str = Form(...),
    event_end_date: str = Form(...)
):
    fields = json.loads(fields)

    if user_uuid != "":
        user = await User.get_or_none(uuid=user_uuid)
        if not user:
            user = None # Sets the user to none if not a user. This should probably be the user's username later
    else:
        user = None

    season = await Season.get_or_none(year=year)
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

    try:
        submission = await MatchScoutingSubmission.create(
            uuid=submission_uuid,
            user=user,
            event=event,
            team_number=team_number,
            match_number=match_number,
            match_type=match_type
        )
    except IntegrityError:
        raise HTTPException(status_code=200, detail="Submission already exists")

    for key, value in fields.items():
        field = await MatchScoutingField.get_or_none(uuid=key)
        if not field:
            raise HTTPException(status_code=404, detail="Field not found")

        _ = await MatchScoutingAnswer.create(
            field=field,
            value=json.dumps(value),
            submission=submission
        )

    return submission