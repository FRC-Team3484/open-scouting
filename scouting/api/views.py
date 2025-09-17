from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.conf import settings

from main.models import Data, Event, PitGroup, Pit

from .permissions import HasUserAPIKey


class StatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                "server_version": settings.SERVER_VERSION,
                "season": str(max(year for year, _ in settings.YEARS)),
                "years": [year for year, _ in settings.YEARS],
            }
        )


class EventListView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year):
        events = Event.objects.filter(year=year).values(
            "event_code", "name", "custom", "custom_data"
        )
        return Response(events)


class EventDetailView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year, event_code):
        event = get_object_or_404(Event, year=year, event_code=event_code)
        data_count = Data.objects.filter(year=year, event_model=event).count()
        pit_group = PitGroup.objects.filter(event=event).first()
        pit_count = Pit.objects.filter(pit_group=pit_group).count()
        return Response(
            {
                "event": {
                    "event_code": event.event_code,
                    "name": event.name,
                    "custom": event.custom,
                    "custom_data": event.custom_data,
                },
                "data_count": data_count,
                "pit_count": pit_count,
            }
        )


class EventDataView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year, event_code):
        qs = Data.objects.filter(year=year, event_code=event_code)
        return Response(list(qs.values()))


class EventPitView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year, event_code):
        event = get_object_or_404(Event, year=year, event_code=event_code)
        pit_group = PitGroup.objects.filter(event=event).first()
        qs = Pit.objects.filter(pit_group=pit_group)
        return Response(list(qs.values()))


class DataYearView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year):
        qs = Data.objects.filter(year=year)
        return Response(list(qs.values()))


class DataTeamView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year, team_number):
        qs = Data.objects.filter(year=year, team_number=team_number)
        return Response(list(qs.values()))


class PitYearView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year):
        events = list(Event.objects.filter(year=year).values_list("id", flat=True))
        pit_groups = list(
            PitGroup.objects.filter(event__in=events).values_list("id", flat=True)
        )
        pits = list(Pit.objects.filter(pit_group__in=pit_groups).values())
        return Response(pits)


class PitTeamView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year, team_number):
        events = list(Event.objects.filter(year=year).values_list("id", flat=True))
        pit_groups = list(
            PitGroup.objects.filter(event__in=events).values_list("id", flat=True)
        )
        pits = list(
            Pit.objects.filter(
                pit_group__in=pit_groups, team_number=team_number
            ).values()
        )
        return Response(pits)


class TeamYearView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year):
        team_numbers = list(
            Data.objects.filter(year=year)
            .values_list("team_number", flat=True)
            .distinct()
        )
        return Response(team_numbers)


class TeamDetailView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year, team_number):
        data_count = Data.objects.filter(year=year, team_number=team_number).count()
        pit_group = PitGroup.objects.filter(year=year).first()
        pit_count = Pit.objects.filter(
            pit_group=pit_group, team_number=team_number
        ).count()
        return Response(
            {
                "team_number": team_number,
                "data_count": data_count,
                "pit_count": pit_count,
            }
        )


class TeamDataView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year, team_number):
        qs = Data.objects.filter(year=year, team_number=team_number)
        return Response(list(qs.values()))


class TeamPitView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, year, team_number):
        pit_group = PitGroup.objects.filter(year=year).first()
        qs = Pit.objects.filter(pit_group=pit_group, team_number=team_number)
        return Response(list(qs.values()))
