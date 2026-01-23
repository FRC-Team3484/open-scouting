from uuid import UUID
from datetime import date, datetime

from typing import Any, override

from tortoise import fields
from tortoise.models import Model
from tortoise.fields.base import Field
from tortoise.fields.relational import ForeignKeyRelation

# Authentication
class User(Model):
    """
    Defines a unique user account on the server

    Attributes:
        uuid (UUID): The unique identifier for the user
        username (str): The username of the user
        email (str): The email address of the user
        hashed_password (str): The hashed password of the user
        is_superuser (bool): Whether the user is a superuser
        created_at (datetime): The date and time the user was created
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    username: Field[str] = fields.CharField(max_length=255, unique=True)
    email: Field[str] = fields.CharField(max_length=255, unique=True)
    hashed_password: Field[str] = fields.CharField(max_length=255)
    is_superuser: Field[bool] = fields.BooleanField(default=False)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

    @override
    def __str__(self) -> str:
        return self.username

class Profile(Model):
    """
    Defines a profile for a user, with cosmetic information not required for basic use on the server

    Attributes:
        uuid (UUID): The unique identifier for the profile
        user (User): The user associated with the profile
        display_name (str): The display name of the user
        team_number (int): The team number of the user
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="profiles")
    display_name: Field[str] = fields.CharField(max_length=255)
    team_number: Field[int] = fields.IntField(null=True)

    @override
    def __str__(self) -> str:
        return self.user.username

class Organization(Model):
    """
    Defines an organization on the server, which is used to offer custom 
        match and pit scouting fields for a team or group of users

    Attributes:
        uuid (UUID): The unique identifier for the organization
        name (str): The name of the organization
        description (str): The description of the organization
        created_at (datetime): The date and time the organization was created
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    name: Field[str] = fields.CharField(max_length=255)
    description: Field[str] = fields.TextField(null=True)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class OrganizationMember(Model):
    """
    Defines a member of an organization, and their role within the organization

    Attributes:
        uuid (UUID): The unique identifier for the organization member
        organization (Organization): The organization the member is a member of
        user (User): The user the member is a member of
        role (str): The role of the member in the organization
        created_at (datetime): The date and time the organization member was created
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    organization: ForeignKeyRelation[Organization] = fields.ForeignKeyField("models.Organization", related_name="members")
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="organizations")
    role: Field[str] = fields.CharField(max_length=255) # member, admin
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class Settings(Model):
    """
    Defines a user's settings on the server

    Each setting is a database field, and should have a default value. 
        These settings do not need to be hardcoded anywhere, other than accessing them in the frontend

    Attributes:
        uuid (UUID): The unique identifier for the settings
        user (User): The user the settings are associated with
        favorite_events (list): The list of favorite events for the user
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="settings")
    favorite_events: Field[Any] = fields.JSONField(null=True, default=list)

# Main
class Season(Model):
    """
    Defines a season on the server. One season should be created for each individual FRC game

    Attributes:
        uuid (UUID): The unique identifier for the season
        year (int): The year of the season
        name (str): The name of the season
        active (bool): Whether the season is active or not
        created_at (datetime): The date and time the season was created
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    year: Field[int] = fields.IntField()
    name: Field[str] = fields.CharField(max_length=255)
    active: Field[bool] = fields.BooleanField(default=True)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

    # Deactivate all other seasons if this one is saved as active
    @override
    async def save(self, *args, **kwargs):
        if self.active:
            await Season.filter(active=True).exclude(uuid=self.uuid).update(active=False)

        await super().save(*args, **kwargs)

class GamePiece(Model):
    """
    Defines a game piece on the server, which is used to specify the game piece used in a field

    Attributes:
        uuid (UUID): The unique identifier for the game piece
        season (Season): The season the game piece is associated with
        name (str): The name of the game piece
        created_at (datetime): The date and time the game piece was created
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField("models.Season", related_name="game_pieces")
    name: Field[str] = fields.CharField(max_length=255)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class MatchScoutingField(Model):
    """
    Defines a single question that should be asked when match scouting for a season

    Attributes:
        uuid (UUID): The unique identifier for the match scouting field
        parent (MatchScoutingField): The parent of the match scouting field
        season (Season): The season the match scouting field is associated with
        name (str): The name of the match scouting field
        field_type (str): The type of the match scouting field
        stat_type (str): The stat type of the match scouting field
        game_piece (GamePiece): The game piece used in the match scouting field
        required (bool): Whether the match scouting field is required or not
        options (list): The options for the match scouting field
        order (int): The order of the match scouting field
        organization (Organization): The organization the match scouting field is associated with
        created_at (datetime): The date and time the match scouting field was created
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    parent: ForeignKeyRelation[MatchScoutingField] | None = fields.ForeignKeyField("models.MatchScoutingField", related_name="children", null=True)
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField("models.Season", related_name="fields")
    name: Field[str] = fields.CharField(max_length=255)
    field_type: Field[str] = fields.CharField(max_length=255) # section, string, large_number, small_number, boolean, choice, multiple_choice
    stat_type: Field[str] = fields.CharField(max_length=255) # section, auton_score, auton_miss, teleop_score, teleop_miss, capability, other, ignore
    game_piece: ForeignKeyRelation[GamePiece] | None = fields.ForeignKeyField("models.GamePiece", related_name="fields", null=True) # needed if stat_type is score or miss
    required: Field[bool] = fields.BooleanField(default=False)
    options: Field[Any] = fields.JSONField(null=True, default=list) # For integer maximum and minimums, choices, etc.
    order: Field[int] = fields.IntField(default=0) # The order the field should appear in the frontend or section
    organization: ForeignKeyRelation[Organization] | None = fields.ForeignKeyField("models.Organization", related_name="scouting_fields", null=True) # Optional, used if the field is specific to an organization
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class Event(Model):
    """
    Defines a single event on the server

    A new object is created for the same event in different years. These are either based on events 
        from TBA, and generated as needed, or generated when a custom event is created

    Attributes:
        uuid (UUID): The unique identifier for the event
        season (Season): The season the event is associated with
        event_code (str): The event code for the event
        name (str): The name of the event
        type (str): The type of the event
        city (str): The city of the event
        country (str): The country of the event
        start_date (date): The start date of the event
        end_date (date): The end date of the event
        pits_generated (bool): Whether the pits for the event have been generated or not
        custom (bool): Whether the event is a custom event or not
        created_at (datetime): The date and time the event was created
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField("models.Season", related_name="events")
    event_code: Field[str] = fields.CharField(max_length=255)
    name: Field[str] = fields.CharField(max_length=255)
    type: Field[str] = fields.CharField(max_length=255)
    city: Field[str] = fields.CharField(max_length=255)
    country: Field[str] = fields.CharField(max_length=255)
    start_date: Field[date] = fields.DateField(null=True)
    end_date: Field[date] = fields.DateField(null=True)
    pits_generated: Field[bool] = fields.BooleanField(default=False)
    custom: Field[bool] = fields.BooleanField(default=False)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class MatchScoutingSubmission(Model):
    """
    Defines a single match scouting submission on the server. This includes the match number
        and team number, and is a single scouting report made up of several answers for the individual fields

    Attributes:
        uuid (UUID): The unique identifier for the match scouting submission
        user (User): The user who submitted the match scouting submission
        event (Event): The event the match scouting submission is associated with
        team_number (int): The team number of the match scouting submission
        match_number (int): The match number of the match scouting submission
        match_type (str): The match type of the match scouting submission
        created_at (datetime): The date and time the match scouting submission was created
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="answers")
    event: ForeignKeyRelation[Event] = fields.ForeignKeyField("models.Event", related_name="answers")
    team_number: Field[int] = fields.IntField(default=0)
    match_number: Field[int] = fields.IntField(default=0)
    match_type: Field[str] = fields.CharField(max_length=255, default="")
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class MatchScoutingAnswer(Model):
    """
    Defines a single match scouting answer for a field. These belong to a MatchScoutingSubmission

    Attributes:
        uuid (UUID): The unique identifier for the match scouting answer
        field (MatchScoutingField): The field the match scouting answer is associated with
        value (str): The value of the match scouting answer
        submission (MatchScoutingSubmission): The match scouting submission the match scouting answer is associated with
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    field: ForeignKeyRelation[MatchScoutingField] = fields.ForeignKeyField("models.MatchScoutingField", related_name="answers")
    value: Field[str] = fields.CharField(max_length=255, null=True)
    submission: ForeignKeyRelation[MatchScoutingSubmission] = fields.ForeignKeyField("models.MatchScoutingSubmission", related_name="answers")

#    Pit Scouting
class PitScoutingField(Model):
    """
    Defines a single question that should be asked when pit scouting for a season

    Attributes:
        uuid (UUID): The unique identifier for the pit scouting field
        season (Season): The season the pit scouting field is associated with
        name (str): The name of the pit scouting field
        field_type (str): The type of the pit scouting field
        options (list): The options for the pit scouting field
        order (int): The order of the pit scouting field
        organization (Organization): The organization the pit scouting field is associated with
        created_at (datetime): The date and time the pit scouting field was created
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField("models.Season", related_name="pit_fields")
    name: Field[str] = fields.CharField(max_length=255)
    field_type: Field[str] = fields.CharField(max_length=255) # text, number, boolean, choice
    options: Field[Any] = fields.JSONField(null=True, default=list) # For field_type=choice
    order: Field[int] = fields.IntField(default=0) # The order the field should appear in the frontend or section
    organization: ForeignKeyRelation[Organization] | None = fields.ForeignKeyField("models.Organization", related_name="pit_fields", null=True) # Optional, used if the field is specific to an organization
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class TeamPit(Model):
    """
    Defines a pit for a single team, per event per season

    Attributes:
        uuid (UUID): The unique identifier for the team pit
        team_number (int): The team number of the team pit
        nickname (str): The nickname of the team pit
        created_at (datetime): The date and time the team pit was created
        season (Season): The season the team pit is associated with
        event (Event): The event the team pit is associated with
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    team_number: Field[int] = fields.IntField()
    nickname: Field[str] = fields.CharField(max_length=255)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField("models.Season", related_name="team_pits")
    event: ForeignKeyRelation[Event] = fields.ForeignKeyField("models.Event", related_name="team_pits")

class PitScoutingAnswer(Model):
    """
    Defines a single pit scouting answer for a pit scouting field. These belong to a TeamPit

    Attributes:
        uuid (UUID): The unique identifier for the pit scouting answer
        field (PitScoutingField): The field the pit scouting answer is associated with
        value (str): The value of the pit scouting answer
        team (TeamPit): The team the pit scouting answer is associated with
        username (str): The username of the user who submitted the pit scouting answer
        created_at (datetime): The date and time the pit scouting answer was created
    """
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    field: ForeignKeyRelation[PitScoutingField] = fields.ForeignKeyField("models.PitScoutingField", related_name="answers")
    value: Field[str] = fields.CharField(max_length=255, null=True)
    team: ForeignKeyRelation[TeamPit] = fields.ForeignKeyField("models.TeamPit", related_name="answers")
    username: Field[str] = fields.CharField(max_length=255, null=True)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)