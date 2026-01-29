import json
from fastapi import APIRouter, HTTPException
from tortoise.exceptions import IntegrityError

from ..models import Event, MatchScoutingAnswer, MatchScoutingField, MatchScoutingSubmission, Season, User
from ..schemas.match_scouting import MatchScoutingRequest, MatchScoutingResponse
from ..utils import get_season

router: APIRouter = APIRouter(
    tags=["Match Scouting"],
)

@router.post("/scouting/submit", response_model=MatchScoutingResponse)
async def submit_match_scouting(
    data: MatchScoutingRequest
) -> MatchScoutingSubmission:
    fields = json.loads(data.fields)

    user: User | None

    if data.user_uuid != "":
        user = await User.get_or_none(uuid=data.user_uuid)
        if not user:
            user = None # Sets the user to none if not a user. This should probably be the user's username later
    else:
        user = None

    season: Season = await get_season(year=data.year)

    event, _ = await Event.get_or_create(
        season=season,
        event_code=data.event_code,
        name=data.event_name,
        type=data.event_type,
        city=data.event_city,
        country=data.event_country,
        start_date=data.event_start_date,
        end_date=data.event_end_date
    )

    try:
        submission: MatchScoutingSubmission = await MatchScoutingSubmission.create(
            uuid=data.submission_uuid,
            user=user,
            event=event,
            team_number=data.team_number,
            match_number=data.match_number,
            match_type=data.match_type
        )
    except IntegrityError:
        raise HTTPException(status_code=200, detail="Submission already exists")

    for key, value in fields.items():
        field: MatchScoutingField | None = await MatchScoutingField.get_or_none(uuid=key)
        if not field:
            raise HTTPException(status_code=404, detail="Field not found")

        _ = await MatchScoutingAnswer.create(
            field=field,
            value=json.dumps(value),
            submission=submission
        )

    return submission