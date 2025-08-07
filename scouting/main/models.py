from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

YEARS = [(2024, "2024"), (2025, "2025")]


# Stores individual contributed data for each year and event
class Data(models.Model):
    uuid = models.UUIDField(null=True, blank=True, verbose_name=_("UUID"))
    year = models.IntegerField(choices=YEARS, verbose_name=_("Year"))
    event = models.CharField(max_length=999, verbose_name=_("Event"))
    event_code = models.CharField(
        max_length=99, blank=True, verbose_name=_("Event Code")
    )
    team_number = models.IntegerField(
        null=True, blank=True, verbose_name=_("Team Number")
    )
    data = models.JSONField(default=dict, blank=True, verbose_name=_("Data"))
    created = models.DateTimeField(null=True, blank=True, verbose_name=_("Created"))
    event_model = models.ForeignKey(
        "Event",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Event"),
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("User Created"),
    )
    username_created = models.CharField(
        max_length=999, blank=True, verbose_name=_("Username Created")
    )
    team_number_created = models.CharField(
        max_length=6, blank=True, verbose_name=_("Team Number Created")
    )
    account = models.BooleanField(default=False, verbose_name=_("Account"))

    def __str__(self):
        if self.team_number:
            return f"{self.team_number}'s data from {self.event} in {self.year}"
        else:
            return f"Data from {self.event} in {self.year}"

    class Meta:
        verbose_name_plural = _("Data")


# Represents an event in a year
class Event(models.Model):
    year = models.IntegerField(choices=YEARS, verbose_name=_("Year"))
    name = models.CharField(max_length=999, verbose_name=_("Name"))
    event_code = models.CharField(
        max_length=99, blank=True, verbose_name=_("Event Code")
    )
    created = models.DateTimeField(null=True, blank=True, verbose_name=_("Created"))
    custom = models.BooleanField(default=False, verbose_name=("Custom"))
    custom_data = models.JSONField(
        default=dict, blank=True, verbose_name=_("Custom Data")
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("User Created"),
    )

    def __str__(self):
        if self.custom:
            return f"{self.name} in {str(self.year)} (Custom event)"
        else:
            return f"{self.name} in {str(self.year)}"


# Represents a group of pits for an event, points to the event
class PitGroup(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name=_("Event"))
    created = models.DateTimeField(null=True, blank=True, verbose_name=_("Created"))
    events_generated = models.BooleanField(
        default=False, verbose_name=_("Events Generated")
    )

    def __str__(self):
        return f"{self.event.name}'s pits"


# Represents a team's pit at an event
class Pit(models.Model):
    uuid = models.UUIDField(null=True, blank=True, verbose_name=_("UUID"))
    team_number = models.CharField(max_length=6, verbose_name=_("Team Number"))
    nickname = models.CharField(max_length=999, blank=True, verbose_name=_("Nickname"))
    pit_group = models.ForeignKey(
        PitGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Pit Group"),
    )
    created = models.DateTimeField(null=True, blank=True, verbose_name=_("Created"))
    data = models.JSONField(default=list, verbose_name=_("Data"))

    def __str__(self):
        if self.pit_group is None:
            return f"{self.team_number}'s pit"
        else:
            return f"{self.team_number}'s pit at {self.pit_group.event.name}"
