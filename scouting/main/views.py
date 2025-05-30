from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q

from main.models import Data, Event, PitGroup, Pit
from . import season_fields
from . import demo_data
from . import pit_scouting_questions

import json
from datetime import datetime
import uuid
from urllib.parse import unquote, urlparse, parse_qs
import requests
import deepdiff

# TODO: This is a duplicate of a similar array in models.py, I don't know if there's a good way to make these into one array
YEARS = ["2024", "2025"]

DATE_FORMAT = "%Y-%m-%d"


# TODO: Move to respective .py files instead
def get_demo_data_from_year(year):
    """
    Returns the demo data for a given year.

    Args:
        year (str): The year that you want the demo data for
    """
    year = str(year)
    if year == "2024":
        return demo_data.crescendo
    elif year == "2025":
        return demo_data.reefscape
    else:
        return None


def get_pit_scouting_questions_from_year(year):
    """
    Returns the pit scouting questions for a given year.

    Args:
        year (str): The year that you want the pit scouting questions for
    """
    year = str(year)
    if year == "2024":
        return pit_scouting_questions.crescendo
    elif year == "2025":
        return pit_scouting_questions.reefscape
    else:
        return None


def decode_json_strings(obj):
    """
    Decodes JSON strings in a dictionary or list

    Args:
        obj (dict, list, or string): The object to decode
    """
    if isinstance(obj, dict):  # If the object is a dictionary
        return {key: decode_json_strings(value) for key, value in obj.items()}
    elif isinstance(obj, list):  # If the object is a list
        return [decode_json_strings(item) for item in obj]
    elif isinstance(obj, str):  # If the object is a string
        return unquote(obj)
    else:  # If it's neither a dictionary, list, nor string, return as is
        return obj


def check_if_event_exists(request, event_name, event_code, year, custom):
    """
    Checks if an event exists and returns it if it does. If not, creates one and
    returns it. Works with custom events.

    Args:
        request (HttpRequest): The request object
        event_name (str): The name of the event
        event_code (str): The event code of the event
        year (str): The year of the event
        custom (bool): Whether the event is custom or not

    Returns:
        Event: The event object
    """
    if type(custom) is not bool:
        custom = (
            json.loads(custom) if custom is not None and custom != "unknown" else False
        )
    else:
        custom = custom

    if custom:
        events = Event.objects.filter(
            name=unquote(event_name),
            event_code=event_code,
            custom=True,
            year=year,
        )

        if len(events) == 0:
            if request.user.is_authenticated:
                event = Event(
                    name=unquote(event_name),
                    event_code=event_code,
                    custom=True,
                    year=year,
                    user_created=request.user,
                )
            else:
                event = Event(
                    name=unquote(event_name),
                    event_code=event_code,
                    custom=True,
                    year=year,
                )

            event.save()
            return event

        else:
            event = events[0]
            return event

    else:
        events = Event.objects.filter(event_code=event_code, year=year)
        if len(events) == 0:
            if request.user.is_authenticated:
                event = Event(
                    year=year,
                    name=unquote(event_name),
                    event_code=event_code,
                    created=timezone.now(),
                    user_created=request.user,
                )
                event.save()
                return event
            else:
                event = Event(
                    year=year,
                    name=unquote(event_name),
                    event_code=event_code,
                    created=timezone.now(),
                )
                event.save()
                return event
        else:
            event = events[0]
            return event


def index(request):
    """
    Returns the index page
    """
    if request.user.is_authenticated:
        context = {
            "SERVER_IP": settings.SERVER_IP,
            "TBA_API_KEY": settings.TBA_API_KEY,
            "YEARS": json.dumps(YEARS),
            "SERVER_MESSAGE": settings.SERVER_MESSAGE,
            "authenticated": json.dumps(True),
            "username": request.user.username,
            "display_name": request.user.profile.display_name,
            "team_number": request.user.profile.team_number,
        }

        return render(request, "index.html", context)

    else:
        context = {
            "SERVER_IP": settings.SERVER_IP,
            "TBA_API_KEY": settings.TBA_API_KEY,
            "YEARS": json.dumps(YEARS),
            "SERVER_MESSAGE": settings.SERVER_MESSAGE,
            "authenticated": json.dumps(False),
        }

        return render(request, "index.html", context)


def contribute(request):
    """
    Returns the contribute page
    """
    request.session["username"] = request.GET.get("username", "unknown")
    request.session["team_number"] = request.GET.get("team_number", "unknown")
    request.session["event_name"] = request.GET.get("event_name", "unknown")
    request.session["event_code"] = request.GET.get("event_code", "unknown")
    request.session["custom"] = request.GET.get("custom", "unknown")
    request.session["year"] = request.GET.get("year", "unknown")
    request.session["demo"] = request.GET.get("demo", "unknown")

    context = {
        "SERVER_IP": settings.SERVER_IP,
        "TBA_API_KEY": settings.TBA_API_KEY,
        "SERVER_MESSAGE": settings.SERVER_MESSAGE,
        "season_fields": json.dumps(
            season_fields.get_season_fields(request.GET.get("year", "unknown"))
        ),
        "username": request.GET.get("username", "unknown"),
        "team_number": request.GET.get("team_number", "unknown"),
        "event_name": request.GET.get("event_name", "unknown"),
        "event_code": request.GET.get("event_code", "unknown"),
        "custom": request.GET.get("custom", "unknown"),
        "year": request.GET.get("year", "unknown"),
        "demo": request.GET.get("demo", "unknown"),
    }

    return render(request, "contribute.html", context)


def data(request):
    """
    Returns the data page
    """
    request.session["username"] = request.GET.get("username", "unknown")
    request.session["team_number"] = request.GET.get("team_number", "unknown")
    request.session["event_name"] = request.GET.get("event_name", "unknown")
    request.session["event_code"] = request.GET.get("event_code", "unknown")
    request.session["custom"] = request.GET.get("custom", "unknown")
    request.session["year"] = request.GET.get("year", "unknown")
    request.session["demo"] = request.GET.get("demo", "unknown")

    context = {
        "SERVER_IP": settings.SERVER_IP,
        "TBA_API_KEY": settings.TBA_API_KEY,
        "SERVER_MESSAGE": settings.SERVER_MESSAGE,
        "username": request.GET.get("username", "unknown"),
        "team_number": request.GET.get("team_number", "unknown"),
        "event_name": request.GET.get("event_name", "unknown"),
        "event_code": request.GET.get("event_code", "unknown"),
        "custom": request.GET.get("custom", "unknown"),
        "year": request.GET.get("year", "unknown"),
        "demo": request.GET.get("demo", "unknown"),
    }

    return render(request, "data.html", context)


def pits(request):
    """
    Returns the pits page
    """
    request.session["username"] = request.GET.get("username", "unknown")
    request.session["team_number"] = request.GET.get("team_number", "unknown")
    request.session["event_name"] = request.GET.get("event_name", "unknown")
    request.session["event_code"] = request.GET.get("event_code", "unknown")
    request.session["custom"] = request.GET.get("custom", "unknown")
    request.session["year"] = request.GET.get("year", "unknown")
    request.session["demo"] = request.GET.get("demo", "unknown")

    context = {
        "SERVER_IP": settings.SERVER_IP,
        "TBA_API_KEY": settings.TBA_API_KEY,
        "SERVER_MESSAGE": settings.SERVER_MESSAGE,
        "username": request.GET.get("username", "unknown"),
        "team_number": request.GET.get("team_number", "unknown"),
        "event_name": request.GET.get("event_name", "unknown"),
        "event_code": request.GET.get("event_code", "unknown"),
        "custom": request.GET.get("custom", "unknown"),
        "year": request.GET.get("year", "unknown"),
        "demo": request.GET.get("demo", "unknown"),
    }

    return render(request, "pits.html", context)


def advanced_data(request):
    """
    Returns the advanced data page
    """
    request.session["username"] = request.GET.get("username", "unknown")
    request.session["team_number"] = request.GET.get("team_number", "unknown")

    context = {
        "SERVER_IP": settings.SERVER_IP,
        "TBA_API_KEY": settings.TBA_API_KEY,
        "SERVER_MESSAGE": settings.SERVER_MESSAGE,
        "YEARS": json.dumps(YEARS),
    }

    return render(request, "advanced_data.html", context)


def service_worker(request):
    """
    Returns the service worker file to the client for installation
    """
    sw_path = settings.BASE_DIR / "frontend" / "sw.js"
    return HttpResponse(open(sw_path).read(), content_type="application/javascript")


def submit(request):
    """
    Submits a scouting report to the server

    Body Parameters:
        uuid: The uuid of the scouting report
        event_name: The name of the event
        event_code: The event code of the event
        year: The year of the event
        custom: Whether or not the event is a custom event
        data: The data of the scouting report
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        event = check_if_event_exists(
            request,
            body["event_name"],
            body["event_code"],
            body["year"],
            body["custom"],
        )

        team_number = next(
            (
                field["value"]
                for field in json.loads(body["data"])
                if field["name"] == "team_number"
            ),
            None,
        )

        if request.user.is_authenticated:
            data = Data(
                uuid=body["uuid"],
                year=body["year"],
                event=unquote(body["event_name"]),
                event_code=body["event_code"],
                data=json.loads(body["data"]),
                created=timezone.now(),
                event_model=event,
                user_created=request.user,
                username_created=request.user.username,
                team_number_created=request.user.profile.team_number,
                account=True,
                team_number=team_number,
            )
            data.save()

        else:
            data = Data(
                uuid=body["uuid"],
                year=body["year"],
                event=unquote(body["event_name"]),
                event_code=body["event_code"],
                data=json.loads(body["data"]),
                created=timezone.now(),
                event_model=event,
                username_created=request.session["username"],
                team_number_created=request.session["team_number"],
                account=False,
                team_number=team_number,
            )
            data.save()

        return HttpResponse(request, "Success")
    else:
        return HttpResponse(request, "Request is not a POST request!", status=501)


def get_data(request):
    """
    Gets the scouting data for an event from the server

    Body Parameters:
        event_name: The name of the event
        event_code: The event code of the event
        year: The year of the event
        custom: Whether or not the event is a custom event
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        if body["demo"] == "true":
            data = get_demo_data_from_year(body["year"])

            data_json = []
            for item in data:
                item_data = {"created": "unknown", "data": item}
                data_json.append(item_data)

            all_names = []
            for entry in data:
                for item in entry:
                    if item["name"] not in all_names:
                        all_names.append(item["name"])

            return JsonResponse(
                {"data": data_json, "data_headers": list(all_names), "demo": True},
                safe=False,
            )

        else:
            event = check_if_event_exists(
                request,
                body["event_name"],
                body["event_code"],
                body["year"],
                body["custom"],
            )

            data = Data.objects.filter(
                year=body["year"],
                event=unquote(body["event_name"]),
                event_code=body["event_code"],
                event_model=event,
            )

            data_json = []
            for item in data:
                item_data = {}
                for key in item.data:
                    try:
                        item_data[key["name"]] = key["value"]
                    except KeyError:
                        break

                item_data["created"] = item.created
                item_data["username_created"] = item.username_created
                item_data["team_number_created"] = item.team_number_created
                item_data["account"] = item.account

                data_json.append(item_data)

            all_names = season_fields.create_tabulator_headers(
                season_fields.collect_field_names(
                    season_fields.get_season_fields(body["year"])
                )
            )

            return JsonResponse(
                {"data": data_json, "data_headers": list(all_names), "demo": False},
                safe=False,
            )

    else:
        return HttpResponse("Request is not a POST request!", status=501)


def get_custom_events(request):
    """
    Gets the custom events from the server for a year

    Body Parameters:
        year: The year of the event
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        data = []

        events = Event.objects.filter(year=body["year"], custom=True)

        for event in events:
            event_data = {
                "custom": True,
                "name": event.name,
                "year": event.year,
                "start_date": event.custom_data["date_begins"],
                "end_date": event.custom_data["date_ends"],
                "location": event.custom_data["location"],
                "type": event.custom_data.get("type", ""),
                "event_code": event.event_code,
            }
            data.append(event_data)

        return JsonResponse(json.dumps(data), safe=False)

    else:
        return HttpResponse("Request is not a POST request!", status=501)


def create_custom_event(request):
    """
    Creates a custom event

    Body Parameters:
        name: The name of the event
        year: The year of the event
        date_begins: The start date of the event
        date_ends: The end date of the event
        location: The location of the event
        type: The type of the event
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        UUID = uuid.uuid4().hex

        data = {
            "name": body["name"],
            "year": body["year"],
            "date_begins": body["date_begins"],
            "date_ends": body["date_ends"],
            "location": body["location"],
            "type": body["type"],
            "event_code": UUID,
        }

        if request.user.is_authenticated:
            event = Event(
                year=data["year"],
                name=body["name"],
                created=timezone.now(),
                event_code=UUID,
                custom=True,
                custom_data=data,
                user_created=request.user,
            )
            event.save()

        else:
            event = Event(
                year=data["year"],
                name=body["name"],
                created=timezone.now(),
                event_code=UUID,
                custom=True,
                custom_data=data,
            )
            event.save()

        return HttpResponse(request, "Success")
    else:
        return HttpResponse(request, "Request is not a POST request!", status=501)


def get_year_data(request):
    """
    Gets the number of events with data for a year

    Body Parameters:
        year: The year of the events to get
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        events = Event.objects.filter(year=body["year"])

        data = {
            "events": len(events),
        }

        return JsonResponse(json.dumps(data), safe=False)

    else:
        return HttpResponse("Request is not a POST request!", status=501)


def check_local_backup_reports(request):
    """
    Checks if local backup reports saved in the client exist on the server

    Body Parameters:
        data: The data to check
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        reports_found = 0
        reports_not_found = 0

        reports_list = json.loads(unquote(body["data"]))

        for report in reports_list:
            data = Data.objects.filter(
                uuid=report["uuid"],
                event_code=report["event_code"],
                year=report["year"],
            )

            if data:
                reports_found += 1
            else:
                reports_not_found += 1

                event = check_if_event_exists(
                    request,
                    report["event_name"],
                    report["event_code"],
                    report["year"],
                    report["custom"],
                )

                if request.user.is_authenticated:
                    new_data = Data(
                        uuid=report["uuid"],
                        year=report["year"],
                        event=unquote(report["event_name"]),
                        event_code=report["event_code"],
                        data=report["data"],
                        created=timezone.now(),
                        event_model=event,
                        user_created=request.user,
                        username_created=request.user.username,
                        team_number_created=request.user.profile.team_number,
                        account=True,
                    )
                    new_data.save()
                else:
                    new_data = Data(
                        uuid=report["uuid"],
                        year=report["year"],
                        event=unquote(report["event_name"]),
                        event_code=report["event_code"],
                        data=report["data"],
                        created=timezone.now(),
                        event_model=event,
                        username_created=request.session["username"],
                        team_number_created=request.session["team_number"],
                        account=False,
                    )
                    new_data.save()

        data = {"reports_found": reports_found, "reports_not_found": reports_not_found}

        return JsonResponse(json.dumps(data), safe=False)

    else:
        return HttpResponse("Request is not a POST request!", status=501)


def upload_offline_reports(request):
    """
    Uploads offline reports saved to the client to the server

    Body Parameters:
        data: The data to upload
    """
    # TODO: This is identical to the previous function, is this necessary or should they be merged into one?
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        reports_found = 0
        reports_not_found = 0

        reports_list = json.loads(unquote(body["data"]))

        for report in reports_list:
            data = Data.objects.filter(
                uuid=report["uuid"],
                event_code=report["event_code"],
                year=report["year"],
            )

            if data:
                reports_found += 1
            else:
                reports_not_found += 1

                event = check_if_event_exists(
                    request,
                    report["event_name"],
                    report["event_code"],
                    report["year"],
                    report["custom"],
                )

                if request.user.is_authenticated:
                    new_data = Data(
                        uuid=report["uuid"],
                        year=report["year"],
                        event=unquote(report["event_name"]),
                        event_code=report["event_code"],
                        data=report["data"],
                        created=timezone.now(),
                        event_model=event,
                        user_created=request.user,
                        username_created=request.user.username,
                        team_number_created=request.user.profile.team_number,
                        account=True,
                    )
                    new_data.save()
                else:
                    new_data = Data(
                        uuid=report["uuid"],
                        year=report["year"],
                        event=unquote(report["event_name"]),
                        event_code=report["event_code"],
                        data=report["data"],
                        created=timezone.now(),
                        event_model=event,
                        username_created=request.session["username"],
                        team_number_created=request.session["team_number"],
                        account=False,
                    )
                    new_data.save()

        data = {"reports_found": reports_found, "reports_not_found": reports_not_found}

        return JsonResponse(json.dumps(data), safe=False)

    else:
        return HttpResponse("Request is not a POST request!", status=501)


def get_pits(request):
    """
    Returns the pits and their data for a given event as JSON

    1. Check if an event exists for this event code and year
    2. Check and see if a pit group has been created for this pit
    3. If the pit group already has pits, they will be returned
    4. If not, the server will attempt to ask TBA for the pits for this event, if none are specified, no pits will be returned and the user will have to manually add them

    Body Parameters:
        event_name: The event name for the event
        event_code: The event code for the event
        year: The year that this event is from
        custom: Whether or not this event is a custom event

    Returns:
        A json dictionary of all the pits for this event and their data
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        event = check_if_event_exists(
            request,
            body["event_name"],
            body["event_code"],
            body["year"],
            body["custom"],
        )

        pit_group = PitGroup.objects.filter(event=event).first()

        if pit_group:
            pits = Pit.objects.filter(pit_group=pit_group)

            pit_data = {
                "event_name": event.name,
                "event_code": event.event_code,
                "year": event.year,
                "custom": event.custom,
                "pits": [],
            }
            for pit in pits:
                pit_entry = {
                    "uuid": pit.uuid,
                    "team_number": pit.team_number,
                    "nickname": pit.nickname,
                    "needs_synced": False,
                    "questions": pit.data,
                }
                pit_data["pits"].append(pit_entry)

            return JsonResponse(pit_data, safe=False, status=200)

        else:
            pit_group = PitGroup.objects.create(
                event=event, created=timezone.now(), events_generated=True
            )
            pit_group.save()

            request_data = {
                "X-TBA-Auth-Key": settings.TBA_API_KEY,
            }

            response = requests.get(
                f"https://www.thebluealliance.com/api/v3/event/{str(body['year'])}{body['event_code']}/teams",
                request_data,
            )

            if response.ok:
                pits_to_create = [
                    Pit(
                        uuid=uuid.uuid4(),
                        team_number=team["team_number"],
                        nickname=team["nickname"],
                        pit_group=pit_group,
                        created=timezone.now(),
                        data=get_pit_scouting_questions_from_year(body["year"]),
                    )
                    for team in response.json()
                ]
                Pit.objects.bulk_create(pits_to_create)

            pits = Pit.objects.filter(pit_group=pit_group)

            pit_data = {
                "event_name": event.name,
                "event_code": event.event_code,
                "year": event.year,
                "custom": event.custom,
                "pits": [],
            }
            for pit in pits:
                pit_entry = {
                    "uuid": pit.uuid,
                    "team_number": pit.team_number,
                    "nickname": pit.nickname,
                    "needs_synced": False,
                    "questions": pit.data,
                }
                pit_data["pits"].append(pit_entry)

            return JsonResponse(pit_data, safe=False, status=200)
    else:
        return HttpResponse(request, "Request is not a POST request!", status=501)


def update_pit(request):
    """
    Takes a single pit from the client and applies the changes to the server pit db

    1. First, checks to see if this pit exists on the server at all. If it doesn't simply add everything to the server and exit, otherwise:
    2. For each question, checks if an answer uuid from the client does not exist in the server
    3. Add the new answers to the server
    4. Checks if there's any new questions with a simple name that does not exist
    5. Add the new questions to the server
    6. Return the updated pit as JSON to the client

    Body Parameters:
        uuid: The uuid of the pit
        event_name: The event name for the event
        event_code: The event code for the event
        year: The year that this event is from
        custom: Whether or not this event is a custom event
        team_number: The team number of the pit
        nickname: The nickname of the pit
        questions: The questions in the pit

    Returns:
        The updated pit as JSON
    """

    if request.method != "POST":
        return HttpResponse("Request is not a POST request!", status=501)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON in request body", status=400)

    pit = Pit.objects.filter(uuid=body["uuid"]).first()
    if not pit:
        # Add new pit if it doesn't exist
        event = check_if_event_exists(
            request,
            body["event_name"],
            body["event_code"],
            body["year"],
            body["custom"],
        )
        pit_group = PitGroup.objects.filter(event=event).first()
        pit = Pit(
            uuid=body["uuid"],
            team_number=body["team_number"],
            nickname=body["nickname"],
            pit_group=pit_group,
            created=timezone.now(),
            data=body["questions"],
        )
        pit.save()

        return JsonResponse(
            {
                "uuid": pit.uuid,
                "team_number": pit.team_number,
                "nickname": pit.nickname,
                "needs_synced": False,
                "questions": pit.data,
            },
            status=200,
        )

    existing_simple_names = {q["simple_name"] for q in pit.data}

    # Add new questions
    for question in body["questions"]:
        if question["simple_name"] not in existing_simple_names:
            pit.data.append(question)

    # Add new answers
    for question in body["questions"]:
        server_question = next(
            (q for q in pit.data if q["simple_name"] == question["simple_name"]), None
        )
        if not server_question:
            continue

        existing_uuids = {a.get("uuid") for a in server_question.get("answers", [])}
        for answer in question.get("answers", []):
            if answer.get("uuid") not in existing_uuids:
                server_question.setdefault("answers", []).append(answer)

    pit.save()

    return JsonResponse(
        {
            "uuid": pit.uuid,
            "team_number": pit.team_number,
            "nickname": pit.nickname,
            "needs_synced": False,
            "questions": pit.data,
        },
        status=200,
    )


def get_pit_questions(request):
    """
    Returns the master list of pit scouting questions for a given year

    Body Parameters:
        year: The year that this event is from

    Returns:
        The master list of pit scouting questions as JSON
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        return JsonResponse(
            get_pit_scouting_questions_from_year(body["year"]),
            safe=False,
            status=200,
        )

    else:
        return HttpResponse(request, "Request is not a POST request!", status=501)


def get_teams_with_filters(request):
    """
    For the advanced data view. For the given year and events, returns a list of all of the teams that match the filters on the server

    Body Parameters:
        year: The year that this event is from
        events: The list of events to filter by

    Returns:
        A list of all of the teams that match the filters as JSON
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            events = [event["code"] for event in json.loads(body["events"])]
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        team_list = []

        if len(events) > 0:
            event_list = Event.objects.filter(event_code__in=events)

            datas = data_list = Data.objects.filter(
                event_model__in=event_list,
                year=body["year"],
            )
            data_list = []

            for data in datas:
                try:
                    if data.team_number not in data_list:
                        data_list.append(data.team_number)
                except (AttributeError, TypeError, KeyError):
                    pass
        else:
            datas = Data.objects.filter(year=body["year"])
            data_list = []

            for data in datas:
                try:
                    if data.team_number not in data_list:
                        data_list.append(data.team_number)
                except (AttributeError, TypeError, KeyError):
                    pass

        for team_number in data_list:
            team_list.append(team_number)

        return JsonResponse(team_list, safe=False, status=200)

    else:
        return HttpResponse(request, "Request is not a POST request!", status=501)


def get_events_with_filters(request):
    """
    For the advanced data view. For the given year and events, returns a list of all of the events in that year
    If teams are specified, only show events where there's data for those teams

    Body Parameters:
        year: The year that this event is from
        teams: The list of teams to filter by

    Returns:
        A list of all of the events that match the filters as JSON
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            teams = json.loads(body["teams"])
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        event_list = []

        if len(teams) > 0:
            events_with_data = Data.objects.filter(
                year=body["year"],
            )

            for data in events_with_data:
                try:
                    for item in data.data:
                        if data.team_number is not None:
                            if str(data.team_number) in teams:
                                if data.event_model.event_code not in event_list:
                                    event_list.append(
                                        {
                                            "name": data.event_model.name,
                                            "code": data.event_model.event_code,
                                        }
                                    )
                                break
                except (AttributeError, TypeError, KeyError):
                    pass

        else:
            events_with_data = Data.objects.filter(year=body["year"])

            for data in events_with_data:
                try:
                    event_info = {
                        "name": data.event_model.name,
                        "code": data.event_model.event_code,
                    }
                    if event_info not in event_list:
                        event_list.append(event_info)
                except AttributeError:
                    pass

        return JsonResponse(event_list, safe=False, status=200)

    else:
        return HttpResponse(request, "Request is not a POST request!", status=501)


def get_data_from_query(request):
    """
    For the advanced data view. Returns a list of all matching data, grouped by teams.

    Example query: `?year=2025&teams=1,2,3&events=alhu,arli`

    Body Parameters:
        query: The query string to filter by

    Returns:
        A list of all data matching the query, grouped by team number.
    """
    if request.method != "POST":
        return HttpResponse("Request is not a POST request!", status=501)

    try:
        body = json.loads(request.body)
        query = urlparse(body.get("query", "")).query
        query_components = parse_qs(query)
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Invalid JSON body", status=400)

    year = query_components.get("year", [None])[0]
    teams = query_components.get("teams", [None])[0]
    events = query_components.get("events", [None])[0]

    if year is None:
        return HttpResponse("No year found in query", status=400)

    # Base query filter by year
    query_filter = Q(year=year)

    # Apply event filter if given
    if events:
        event_list = events.split(",")
        query_filter &= Q(event_model__event_code__in=event_list)

    # Get initial queryset (filtered only by year and events)
    data_queryset = Data.objects.filter(query_filter)

    # Manually filter by teams since JSON filtering is not supported in SQLite
    team_list = teams.split(",") if teams else []
    filtered_data = []

    for item in data_queryset:
        team_number = None

        if not team_list or str(item.team_number) in team_list:
            if isinstance(item.data, list):
                for field in item.data:
                    field.setdefault("stat_type", "ignore")
                    field.setdefault("game_piece", "")
            filtered_data.append(item)

    # Organize results by team
    team_data_map = {}

    for item in filtered_data:
        team_number = str(item.team_number)
        if team_number:
            team_data_map.setdefault(team_number, []).append(item.data)

    final_data = [
        {"team_number": team, "data": fields} for team, fields in team_data_map.items()
    ]

    return JsonResponse(final_data, safe=False, status=200)


@csrf_exempt
def get_version(request):
    if request.method == "POST":
        return JsonResponse(
            {"version": settings.SERVER_VERSION}, safe=False, status=200
        )
    else:
        return HttpResponse("Request is not a POST request!", status=501)
