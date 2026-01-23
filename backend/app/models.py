from uuid import UUID
from datetime import date, datetime

from typing import Any, override

from tortoise import fields
from tortoise.models import Model
from tortoise.fields.base import Field
from tortoise.fields.relational import ForeignKeyRelation

# Authentication
class User(Model):
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
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="profiles")
    display_name: Field[str] = fields.CharField(max_length=255)
    team_number: Field[int] = fields.IntField(null=True)

    @override
    def __str__(self) -> str:
        return self.user.username

class Organization(Model):
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    name: Field[str] = fields.CharField(max_length=255)
    description: Field[str] = fields.TextField(null=True)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class OrganizationMember(Model):
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    organization: ForeignKeyRelation[Organization] = fields.ForeignKeyField("models.Organization", related_name="members")
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="organizations")
    role: Field[str] = fields.CharField(max_length=255) # member, admin
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class Settings(Model):
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="settings")
    favorite_events: Field[Any] = fields.JSONField(null=True, default=list)

# Main
class Season(Model):
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
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField("models.Season", related_name="game_pieces")
    name: Field[str] = fields.CharField(max_length=255)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class MatchScoutingField(Model):
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
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="answers")
    event: ForeignKeyRelation[Event] = fields.ForeignKeyField("models.Event", related_name="answers")
    team_number: Field[int] = fields.IntField(default=0)
    match_number: Field[int] = fields.IntField(default=0)
    match_type: Field[str] = fields.CharField(max_length=255, default="")
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class MatchScoutingAnswer(Model):
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    field: ForeignKeyRelation[MatchScoutingField] = fields.ForeignKeyField("models.MatchScoutingField", related_name="answers")
    value: Field[str] = fields.CharField(max_length=255, null=True)
    submission: ForeignKeyRelation[MatchScoutingSubmission] = fields.ForeignKeyField("models.MatchScoutingSubmission", related_name="answers")

#    Pit Scouting
# A PitScoutingField is defined in the admin interface
# When the pits list for a season and event is fetched, create it, and attempt to populate the teams in it from TBA
# Then the questions for that season (PitScoutingField) are loaded, and appear for each TeamPit
# New TeamPits can be created, and when an answer is added, create a PitScoutingAnswer
class PitScoutingField(Model):
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField("models.Season", related_name="pit_fields")
    name: Field[str] = fields.CharField(max_length=255)
    field_type: Field[str] = fields.CharField(max_length=255) # text, number, boolean, choice
    options: Field[Any] = fields.JSONField(null=True, default=list) # For field_type=choice
    order: Field[int] = fields.IntField(default=0) # The order the field should appear in the frontend or section
    organization: ForeignKeyRelation[Organization] | None = fields.ForeignKeyField("models.Organization", related_name="pit_fields", null=True) # Optional, used if the field is specific to an organization
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)

class TeamPit(Model):
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    team_number: Field[int] = fields.IntField()
    nickname: Field[str] = fields.CharField(max_length=255)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField("models.Season", related_name="team_pits")
    event: ForeignKeyRelation[Event] = fields.ForeignKeyField("models.Event", related_name="team_pits")

class PitScoutingAnswer(Model):
    uuid: Field[UUID] = fields.UUIDField(pk=True)
    field: ForeignKeyRelation[PitScoutingField] = fields.ForeignKeyField("models.PitScoutingField", related_name="answers")
    value: Field[str] = fields.CharField(max_length=255, null=True)
    team: ForeignKeyRelation[TeamPit] = fields.ForeignKeyField("models.TeamPit", related_name="answers")
    username: Field[str] = fields.CharField(max_length=255, null=True)
    created_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)