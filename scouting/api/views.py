from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.shortcuts import get_object_or_404
from django.conf import settings

from main.models import Data, Event, PitGroup, Pit
from .permissions import HasUserAPIKey
from .serializers import (
    DataSerializer,
    EventSerializer,
    PitSerializer,
    TeamNumberSerializer,
)


class StatusView(APIView):
    """
    Returns server version, season, and years
    """

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                "server_version": settings.SERVER_VERSION,
                "season": str(max(year for year, _ in settings.YEARS)),
                "years": [year for year, _ in settings.YEARS],
            }
        )


class EventListView(ListAPIView):
    """
    Returns all events for a given year (paginated)
    """

    serializer_class = EventSerializer
    permission_classes = [HasUserAPIKey]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Event.objects.filter(year=self.kwargs["year"])


class EventDetailView(APIView):
    """
    Returns event information, as well as data and pit count for a given event
    """

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


class EventDataView(ListAPIView):
    """
    Returns all data for a given event (paginated)
    """

    serializer_class = DataSerializer
    permission_classes = [HasUserAPIKey]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Data.objects.filter(
            year=self.kwargs["year"], event_code=self.kwargs["event_code"]
        )


class EventPitView(ListAPIView):
    """
    Returns all pits for a given event (paginated)
    """

    serializer_class = PitSerializer
    permission_classes = [HasUserAPIKey]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        event = get_object_or_404(
            Event, year=self.kwargs["year"], event_code=self.kwargs["event_code"]
        )
        pit_group = PitGroup.objects.filter(event=event).first()
        return Pit.objects.filter(pit_group=pit_group)


class DataYearView(ListAPIView):
    """
    Returns all data for a given year (paginated)
    """

    serializer_class = DataSerializer
    permission_classes = [HasUserAPIKey]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Data.objects.filter(year=self.kwargs["year"])


class DataTeamView(ListAPIView):
    """
    Returns all data for a given team (paginated)
    """

    serializer_class = DataSerializer
    permission_classes = [HasUserAPIKey]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Data.objects.filter(
            year=self.kwargs["year"], team_number=self.kwargs["team_number"]
        )


class PitYearView(ListAPIView):
    """
    Returns all pits for a given year (paginated)
    """

    serializer_class = PitSerializer
    permission_classes = [HasUserAPIKey]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        events = Event.objects.filter(year=self.kwargs["year"])
        pit_groups = PitGroup.objects.filter(event__in=events)
        return Pit.objects.filter(pit_group__in=pit_groups)


class PitTeamView(ListAPIView):
    """
    Returns all pits for a given team (paginated)
    """

    serializer_class = PitSerializer
    permission_classes = [HasUserAPIKey]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        events = Event.objects.filter(year=self.kwargs["year"])
        pit_groups = PitGroup.objects.filter(event__in=events)
        return Pit.objects.filter(
            pit_group__in=pit_groups, team_number=self.kwargs["team_number"]
        )


class TeamYearView(ListAPIView):
    """
    Returns all team numbers for a given year (paginated)
    """

    serializer_class = TeamNumberSerializer
    permission_classes = [HasUserAPIKey]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return (
            Data.objects.filter(year=self.kwargs["year"])
            .values("team_number")
            .distinct()
        )


class TeamDetailView(APIView):
    """Returns data and pit count for a given team"""

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


class TeamDataView(ListAPIView):
    """
    Returns all data for a given team (paginated)
    """

    serializer_class = DataSerializer
    permission_classes = [HasUserAPIKey]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Data.objects.filter(
            year=self.kwargs["year"], team_number=self.kwargs["team_number"]
        )


class TeamPitView(ListAPIView):
    """
    Returns all pits for a given team (paginated)
    """

    serializer_class = PitSerializer
    permission_classes = [HasUserAPIKey]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        pit_group = PitGroup.objects.filter(year=self.kwargs["year"]).first()
        return Pit.objects.filter(
            pit_group=pit_group, team_number=self.kwargs["team_number"]
        )
