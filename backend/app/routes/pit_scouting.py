from collections import defaultdict
import os
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import Identity, get_identity, require_superuser
from ..models import PitScoutingAnswer, Season, TeamPit
from ..schemas.generic import MessageResponse
from ..schemas.pit_scouting import AdminPitResponse, GetPitsResponse, PitAnswerResponse, SubmitPitFieldAnswerRequest
from ..utils import get_event, get_season, IS_DEV


router: APIRouter = APIRouter(
    tags=["Pit Scouting"],
    include_in_schema=IS_DEV
)

TBA_API_KEY = os.getenv("TBA_API_KEY")

@router.post("/pits/get/{season_uuid}/{event_code}", response_model=list[GetPitsResponse])
async def get_pits(
        season_uuid: UUID,
        event_code: str,
        identity: Identity = Depends(get_identity)
    )-> list[GetPitsResponse]:
    """
    Get all pits for a season and event

    Parameters:
        season_uuid (`UUID`): The UUID of the season to get pits for
        data (`GetPitsForSeasonRequest`): The UUID of the season to get pits for

    Returns:
        list: A list of all pits for the season
    """
    season: Season = await get_season(season_uuid)

    event, created = await get_event(season.year, event_code)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if created and identity.session is not None:
        event.created_by = identity.session
        await event.save()

    # If pits have not been generated yet, get teams from TBA and create TeamPits
    if not event.pits_generated and TBA_API_KEY != "" and TBA_API_KEY is not None and event.custom == False:
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
                event=event,
                created_by=identity.session
            )

        event.pits_generated = True
        await event.save()

    pits: list[TeamPit] = await TeamPit.filter(event=event).prefetch_related("answers")
    return [
        GetPitsResponse(
            uuid=pit.uuid,
            team_number=pit.team_number,
            nickname=pit.nickname,
            created_at=pit.created_at,
            answers=[
                PitAnswerResponse(
                    uuid=ans.uuid,
                    field_uuid=ans.field_id,
                    value=ans.value,
                    username=ans.username,
                    created_at=ans.created_at
                )
                for ans in pit.answers
            ]
        )
        for pit in pits
    ]

@router.post("/pits/submit/{season_uuid}/{team_number}", response_model=MessageResponse)
async def submit_pit(
        season_uuid: UUID,
        team_number: int,
        data: SubmitPitFieldAnswerRequest,
        identity: Identity = Depends(require_superuser)
    ):
    """
    Get the season and event from the uuids. Then, check if a pit with that team number exists.
    If it does, update that pit

    For the answers in that pit, find each answer that does not already exist on the server, and add them

    If a pit does not exist, that means it was created by the client of a user. It should be created.

    Parameters:
        season_uuid (`UUID`): The UUID of the season to get pits for
        team_number (`int`): The team number to get pits for
        data (`SubmitPitFieldAnswerRequest`): The UUID of the season and event to get pits for

    Returns:
        MessageResponse: A message indicating that the pits were submitted
    """
    
    season: Season = await get_season(season_uuid)

    event, _ = await get_event(season.year, data.event_code)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    pit, created = await TeamPit.get_or_create(
        uuid=data.uuid,
        team_number=team_number,
        season=season,
        event=event,
        nickname=data.nickname,
    )

    if created:
        pit.created_by = identity.session

        # Pit was created on client, attempt to fetch nickname
        if not data.nickname:
            if TBA_API_KEY != "" and TBA_API_KEY is not None and event.custom == False:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(
                        f"https://www.thebluealliance.com/api/v3/team/frc{team_number}",
                        headers={"X-TBA-Auth-Key": TBA_API_KEY},
                    )

                if response.status_code == 200:
                    pit.nickname = response.json()["nickname"]

        await pit.save()
        print("Created pit", pit.uuid, "for team", team_number, "and event", event.uuid)

    for answer in data.answers:
        field = await PitScoutingField.get_or_none(uuid=answer["field_uuid"])

        if not field:
            raise HTTPException(status_code=404, detail="Field not found")

        answer_object, created = await PitScoutingAnswer.get_or_create(
            uuid=answer["uuid"],
            team=pit,
            field=field,
            value=answer["value"],
            username=answer["username"]
        )

        if created:
            answer_object.created_by = identity.session
            await answer_object.save()
            print("Created answer", answer["uuid"], "for pit", pit.uuid, "and field", field.uuid)

    return {"message": "Pit submitted successfully"}

@router.get("/pits/get", response_model=list[AdminPitResponse])
async def get_all_pits(identity: Identity = Depends(require_superuser)) -> list[AdminPitResponse]:
    """
    Get all pits

    Requires superuser access

    Returns:
        list[AdminPitResponse]: A list of all pits
    """
    answers = defaultdict(int)

    for pit_id in await PitScoutingAnswer.all().values_list(
        "team_id", flat=True
    ):
        answers[pit_id] += 1

    return [
        AdminPitResponse(
            uuid=pit.uuid, 
            event_name=getattr(pit.event, "name", "N/A"),
            event_code=getattr(pit.event, "event_code", "N/A"),
            team_number=pit.team_number, 
            answers=answers[pit.uuid],
            created_at=pit.created_at
        ) for pit in await TeamPit.all().select_related("event")
    ]

@router.delete("/pits/delete/{pit_uuid}", response_model=MessageResponse)
async def delete_pit(pit_uuid: UUID, identity: Identity = Depends(require_superuser)) -> MessageResponse:
    """
    Delete a pit

    Requires superuser access

    Parameters:
        pit_uuid (`UUID`): The UUID of the pit to delete

    Returns:
        MessageResponse: A message indicating that the pit was deleted
    """
    await TeamPit.filter(uuid=pit_uuid).delete()
    return MessageResponse(message="Pit deleted")