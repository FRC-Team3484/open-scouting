from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import Identity, require_user
from ..models import MatchScoutingAnswer, MatchScoutingSubmission, PitScoutingAnswer, Session, TeamPit, Event
from ..schemas.generic import MessageResponse
from ..schemas.profile import MyDataResponse, MyDataTypes
from ..utils import IS_DEV


router: APIRouter = APIRouter(
    tags=["Profile"],
    include_in_schema=IS_DEV
)

@router.get("/profile/my_data", response_model=list[MyDataResponse])
async def get_my_data(identity: Identity = Depends(require_user)):
    """
    Return data that the user has submitted

    This includes MatchScoutingSubmission, MatchScoutingAnswer, TeamPit, PitScoutingAnswer end Event models created by the user

    First, get every MatchScoutingSubmission, MatchScoutingAnswer, TeamPit, PitScoutingAnswer and 
        Event model that has a created_by session that is owned by the user

    Returns:
        list[MyDataResponse]: A list of data that the user has submitted
    """
    sessions = await Session.filter(user=identity.user)
    session_uuids = [session.uuid for session in sessions]

    data: list[MyDataResponse] = []

    match_scouting_submissions = await MatchScoutingSubmission.filter(created_by_id__in=session_uuids).all()
    match_scouting_answers = await (MatchScoutingAnswer.filter(created_by_id__in=session_uuids).prefetch_related("field")).all()
    team_pits = await (TeamPit.filter(created_by_id__in=session_uuids).prefetch_related("event")).all()
    pit_scouting_answers = await (PitScoutingAnswer.filter(created_by_id__in=session_uuids).prefetch_related("field")).all()
    events = await Event.filter(created_by_id__in=session_uuids, custom=True).all()

    for submission in match_scouting_submissions:
        data.append(
            MyDataResponse(
                uuid=submission.uuid,
                type="match_scouting_submission",
                name=f"Match Scouting Submission for team {submission.team_number} in {submission.match_type} match {submission.match_number}",
                created_at=submission.created_at
            )
        )

    for answer in match_scouting_answers:
        data.append(
            MyDataResponse(
                uuid=answer.uuid,
                type="match_scouting_answer",
                name=f"Match Scouting Answer {answer.value} for field \"{answer.field.name}\"",
                created_at=answer.created_at
            )
        )

    for team_pit in team_pits:
        data.append(
            MyDataResponse(
                uuid=team_pit.uuid,
                type="team_pit",
                name=f"Team Pit for team {team_pit.team_number} at event \"{team_pit.event.name}\"",
                created_at=team_pit.created_at
            )
        )

    for answer in pit_scouting_answers:
        data.append(
            MyDataResponse(
                uuid=answer.uuid,
                type="pit_scouting_answer",
                name=f"Pit Scouting Answer '{answer.value}' for \"{answer.field.name}\"",
                created_at=answer.created_at
            )
        )

    for event in events:
        data.append(
            MyDataResponse(
                uuid=event.uuid,
                type="event",
                name=f"Custom Event \"{event.name}\"",
                created_at=event.created_at
            )
        )

    return data

@router.delete("/profile/delete/{type}/{uuid}", response_model=MessageResponse)
async def delete_my_data(type: MyDataTypes, uuid: UUID, identity: Identity = Depends(require_user)):
    """
    Given type and uuid, delete the data that the user has submitted

    Ensure that the user has created the data before deleting it

    Parameters:
        type (MyDataTypes): The type of data to delete
        uuid (UUID): The uuid of the data to delete

    Returns:
        MessageResponse: A message indicating that the data was deleted
    """
    if type == "match_scouting_submission":
        submission: MatchScoutingSubmission | None = await (MatchScoutingSubmission.filter(uuid=uuid).select_related("created_by__user").get_or_none())
        if not submission:
            raise HTTPException(status_code=404, detail="MatchScoutingSubmission not found")

        if submission.created_by.user != identity.user:
            raise HTTPException(status_code=403, detail="You do not have permission to delete this MatchScoutingSubmission")
            
        await submission.delete()
        return MessageResponse(message="MatchScoutingSubmission deleted")

    elif type == "match_scouting_answer":
        match_scouting_answer: MatchScoutingAnswer | None = await (MatchScoutingAnswer.filter(uuid=uuid).select_related("created_by__user").get_or_none())
        if not match_scouting_answer:
            raise HTTPException(status_code=404, detail="MatchScoutingAnswer not found")

        if match_scouting_answer.created_by.user != identity.user:
            raise HTTPException(status_code=403, detail="You do not have permission to delete this MatchScoutingAnswer")

        await match_scouting_answer.delete()
        return MessageResponse(message="MatchScoutingAnswer deleted")

    elif type == "team_pit":
        team_pit: TeamPit | None = await (TeamPit.filter(uuid=uuid).select_related("created_by__user").get_or_none())
        if not team_pit:
            raise HTTPException(status_code=404, detail="TeamPit not found")

        if team_pit.created_by.user != identity.user:
            raise HTTPException(status_code=403, detail="You do not have permission to delete this TeamPit")

        await team_pit.delete()
        return MessageResponse(message="TeamPit deleted")

    elif type == "pit_scouting_answer":
        pit_scouting_answer: PitScoutingAnswer | None = await (PitScoutingAnswer.filter(uuid=uuid).select_related("created_by__user").get_or_none())
        if not pit_scouting_answer:
            raise HTTPException(status_code=404, detail="PitScoutingAnswer not found")

        if pit_scouting_answer.created_by.user != identity.user:
            raise HTTPException(status_code=403, detail="You do not have permission to delete this PitScoutingAnswer")

        await pit_scouting_answer.delete()
        return MessageResponse(message="PitScoutingAnswer deleted")

    elif type == "event":
        event: Event | None = await (Event.filter(uuid=uuid).select_related("created_by__user").get_or_none())
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if event.created_by.user != identity.user:
            raise HTTPException(status_code=403, detail="You do not have permission to delete this Event")

        await event.delete()
        return MessageResponse(message="Event deleted")
