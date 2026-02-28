from collections import defaultdict
import json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import IntegrityError

from ..dependencies import require_superuser
from ..schemas.generic import MessageResponse
from ..models import Event, MatchScoutingAnswer, MatchScoutingField, MatchScoutingSubmission, Season, User
from ..schemas.match_scouting import MatchScoutingRequest, MatchScoutingResponse, SubmissionResponse
from ..utils import get_season, IS_DEV


router: APIRouter = APIRouter(
    tags=["Match Scouting"],
    include_in_schema=IS_DEV
)

@router.post("/scouting/submit", response_model=MatchScoutingResponse)
async def submit_match_scouting(
    data: MatchScoutingRequest
) -> MatchScoutingResponse:
    """
    Submit a match scouting form

    Will create a MatchScoutingSubmission for each submission, and then create a MatchScoutingAnswer for each field answer

    Parameters:
        data (MatchScoutingRequest): The data to submit the match scouting form

    Returns:
        `MatchScoutingSubmission`: The submitted match scouting form
    """
    fields = data.fields

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

    return MatchScoutingResponse(
        uuid=submission.uuid,
        user=submission.user.uuid if submission.user else None,
        event=submission.event.uuid,
        team_number=submission.team_number,
        match_number=submission.match_number,
        match_type=submission.match_type,
        created_at=submission.created_at
    )

@router.get("/scouting/submissions", response_model=list[SubmissionResponse])
async def get_match_scouting_submissions(superuser = Depends(require_superuser)) -> list[SubmissionResponse]:
    """
    Get all match scouting submissions

    Requires superuser access

    Returns:
        list[SubmissionResponse]: A list of all match scouting submissions
    """
    answers = defaultdict(int)

    for submission_id in await MatchScoutingAnswer.all().values_list(
        "submission_id", flat=True
    ):
        answers[submission_id] += 1

    return [
        SubmissionResponse(
            uuid=submission.uuid,
            event_name=submission.event.name,
            event_code=submission.event.event_code,
            team_number=submission.team_number,
            match_number=submission.match_number,
            match_type=submission.match_type,
            answers=answers[submission.uuid],
            created_at=submission.created_at
        ) for submission in await MatchScoutingSubmission.all().select_related("event")
    ]

@router.delete("/scouting/submissions/delete/{submission_uuid}", response_model=MessageResponse)
async def delete_match_scouting_submission(submission_uuid: UUID, superuser = Depends(require_superuser)) -> MessageResponse:
    """
    Delete a match scouting submission

    Requires superuser access

    Parameters:
        submission_uuid (`UUID`): The UUID of the submission to delete

    Returns:
        MessageResponse: A message indicating that the submission was deleted
    """
    await MatchScoutingSubmission.filter(uuid=submission_uuid).delete()
    return MessageResponse(message="Submission deleted")