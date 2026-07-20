from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException


from ..dependencies import Identity, get_identity, require_superuser
from ..models import Event, MatchScoutingAnswer, MatchScoutingSubmission, PitScoutingAnswer, Report, TeamPit
from ..schemas.generic import MessageResponse
from ..schemas.reports import CreateReportRequest, CreateReportResponse, EventReportDetails, MatchScoutingAnswerReportDetails, MatchScoutingSubmissionReportDetails, PitScoutingAnswerReportDetails, ReportResponse, TeamPitReportDetails
from ..utils import IS_DEV


router: APIRouter = APIRouter(
    tags=["Reports"],
    include_in_schema=IS_DEV
)

@router.post("/report/create", response_model=CreateReportResponse)
async def create_report(data: CreateReportRequest, identity: Identity = Depends(get_identity)):
    """
    Create a new report

    Parameters:
        data (CreateReportRequest): The data to create the report

    Returns:
        `CreateReportResponse`: The created report
    """
    report: Report = await Report.create(
        type=data.type,
        content_uuid=data.content_uuid,
        report_reason=data.report_reason,
        report_details=data.report_details,
        created_by=identity.session
    )

    return CreateReportResponse(
        uuid=report.uuid,
        type=report.type,
        content_uuid=report.content_uuid,
        report_reason=report.report_reason,
        report_details=report.report_details
    )

@router.get("/reports/get", response_model=list[ReportResponse])
async def get_reports(identity: Identity = Depends(require_superuser)):
    """
    Get all reports from the server

    Construct corresponding report_details depending on the type of each report

    Requires superuser access

    Returns:
        list[ReportResponse]: A list of all reports
    """
    if not identity.user or not identity.user.is_superuser:
        raise HTTPException(status_code=403, detail="Superuser required")

    reports: list[Report] = await Report.all()
    response: list[ReportResponse] = []

    for report in reports:
        content_details: MatchScoutingSubmissionReportDetails | MatchScoutingAnswerReportDetails | TeamPitReportDetails | PitScoutingAnswerReportDetails | EventReportDetails | None = None

        if report.type == "match_scouting_submission":
            match_scouting_submission = await MatchScoutingSubmission.get(uuid=report.content_uuid)

            if match_scouting_submission:
                await match_scouting_submission.fetch_related("answers", "event", "event__season")

                answer_details: list[MatchScoutingAnswerReportDetails] = []

                for answer in match_scouting_submission.answers:
                    await answer.fetch_related("field")

                    answer_details.append(
                        MatchScoutingAnswerReportDetails(
                            uuid=answer.uuid,
                            field_uuid=answer.field.uuid,
                            value=answer.value,
                            created_at=answer.created_at
                        )
                    )

                content_details = MatchScoutingSubmissionReportDetails(
                    uuid=match_scouting_submission.uuid,
                    event_uuid=match_scouting_submission.event.uuid,
                    season_uuid=match_scouting_submission.event.season.uuid,
                    team_number=match_scouting_submission.team_number,
                    match_number=match_scouting_submission.match_number,
                    match_type=match_scouting_submission.match_type,
                    answers_count=len(match_scouting_submission.answers),
                    answers=answer_details
                )

        elif report.type == "match_scouting_answer":
            match_scouting_answer = await MatchScoutingAnswer.get(uuid=report.content_uuid)

            if match_scouting_answer:
                await match_scouting_answer.fetch_related("field")

                content_details = MatchScoutingAnswerReportDetails(
                    uuid=match_scouting_answer.uuid,
                    field_uuid=match_scouting_answer.field.uuid,
                    value=match_scouting_answer.value,
                    created_at=match_scouting_answer.created_at
                )

        elif report.type == "team_pit":
            team_pit = await TeamPit.get(uuid=report.content_uuid)

            if team_pit:
                await team_pit.fetch_related("event", "event__season")

                content_details = TeamPitReportDetails(
                    uuid=team_pit.uuid,
                    team_number=team_pit.team_number,
                    nickname=team_pit.nickname,
                    season_uuid=team_pit.event.season.uuid,
                    event_uuid=team_pit.event.uuid
                )

        elif report.type == "pit_scouting_answer":
            pit_scouting_answer = await PitScoutingAnswer.get(uuid=report.content_uuid)

            if pit_scouting_answer:
                await pit_scouting_answer.fetch_related("field", "team")

                content_details = PitScoutingAnswerReportDetails(
                    uuid=pit_scouting_answer.uuid,
                    field_uuid=pit_scouting_answer.field.uuid,
                    value=pit_scouting_answer.value,
                    team_uuid=pit_scouting_answer.team.uuid,
                    team_number=pit_scouting_answer.team.team_number,
                    created_at=pit_scouting_answer.created_at
                )

        elif report.type == "event":
            event = await Event.get(uuid=report.content_uuid)

            if event:
                await event.fetch_related("season")

                content_details = EventReportDetails(
                    uuid=event.uuid,
                    season_uuid=event.season.uuid,
                    event_code=event.event_code,
                    name=event.name,
                    type=event.type,
                    city=event.city,
                    country=event.country,
                    start_date=event.start_date,
                    end_date=event.end_date,
                    custom=event.custom,
                    created_at=event.created_at
                )

        response.append(ReportResponse(
            uuid=report.uuid,
            type=report.type,
            content_uuid=report.content_uuid,
            content_details=content_details,
            report_reason=report.report_reason,
            report_details=report.report_details,
            created_at=report.created_at
        ))

    return response

@router.get("/reports/get/count", response_model=int)
async def get_reports_count(identity: Identity = Depends(require_superuser)):
    """
    Get the number of reports

    Requires superuser access

    Returns:
        CountResponse: The number of reports
    """
    if not identity.user or not identity.user.is_superuser:
        raise HTTPException(status_code=403, detail="Superuser required")

    return await Report.all().count()

@router.delete("/report/content/delete/{report_uuid}", response_model=MessageResponse)
async def delete_report_content(report_uuid: UUID, identity: Identity = Depends(require_superuser)):
    """
    Delete the content for a report. Then delete the report itself.

    Requires superuser access

    Parameters:
        report_uuid (`UUID`): The UUID of the report's content to delete

    Returns:
        MessageResponse: A message indicating that the report was deleted
    """
    if not identity.user or not identity.user.is_superuser:
        raise HTTPException(status_code=403, detail="Superuser required")

    report = await Report.get_or_none(uuid=report_uuid)

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.type == "match_scouting_submission":
        match_scouting_submission = await MatchScoutingSubmission.get_or_none(uuid=report.content_uuid)

        if match_scouting_submission:
            await match_scouting_submission.delete()
        else:
            raise HTTPException(status_code=404, detail="Match scouting submission not found")

    elif report.type == "match_scouting_answer":
        match_scouting_answer = await MatchScoutingAnswer.get_or_none(uuid=report.content_uuid)

        if match_scouting_answer:
            await match_scouting_answer.delete()
        else:
            raise HTTPException(status_code=404, detail="Match scouting answer not found")

    elif report.type == "team_pit":
        team_pit = await TeamPit.get_or_none(uuid=report.content_uuid)

        if team_pit:
            await team_pit.delete()
        else:
            raise HTTPException(status_code=404, detail="Team pit not found")

    elif report.type == "pit_scouting_answer":
        pit_scouting_answer = await PitScoutingAnswer.get_or_none(uuid=report.content_uuid)

        if pit_scouting_answer:
            await pit_scouting_answer.delete()
        else:
            raise HTTPException(status_code=404, detail="Pit scouting answer not found")

    elif report.type == "event":
        event = await Event.get_or_none(uuid=report.content_uuid)

        if event:
            await event.delete()
        else:
            raise HTTPException(status_code=404, detail="Event not found")

    await report.delete()

    return MessageResponse(message="Report deleted")

@router.delete("/report/delete/{report_uuid}", response_model=MessageResponse)
async def delete_report(report_uuid: UUID, identity: Identity = Depends(require_superuser)) -> MessageResponse:
    """
    Delete a report

    Requires superuser access

    Parameters:
        report_uuid (`UUID`): The UUID of the report to delete

    Returns:
        MessageResponse: A message indicating that the report was deleted
    """
    if not identity.user or not identity.user.is_superuser:
        raise HTTPException(status_code=403, detail="Superuser required")

    report = await Report.get_or_none(uuid=report_uuid)

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    await report.delete()
    return MessageResponse(message="Report deleted")