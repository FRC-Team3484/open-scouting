from venv import create
from tortoise.fields.base import Field


from datetime import datetime


from re import M
from tortoise import fields
from tortoise.models import Model

# Authentication
class User(Model):
    uuid = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_superuser = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Profile(Model):
    uuid = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="profiles")
    display_name = fields.CharField(max_length=255)
    team_number = fields.IntField(null=True)

    def __str__(self):
        return self.user

class Organization(Model):
    uuid = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class OrganizationMember(Model):
    uuid = fields.UUIDField(pk=True)
    organization = fields.ForeignKeyField("models.Organization", related_name="members")
    user = fields.ForeignKeyField("models.User", related_name="organizations")
    role = fields.CharField(max_length=255) # member, admin
    created_at = fields.DatetimeField(auto_now_add=True)

class Settings(Model):
    uuid = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="settings")
    favorite_events = fields.JSONField(null=True, default=list)

# Main
class Season(Model):
    uuid = fields.UUIDField(pk=True)
    year = fields.IntField()
    name = fields.CharField(max_length=255)
    active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    # Deactivate all other seasons if this one is saved as active
    async def save(self, *args, **kwargs):
        if self.active:
            await Season.filter(active=True).exclude(uuid=self.uuid).update(active=False)

        await super().save(*args, **kwargs)

class GamePiece(Model):
    uuid = fields.UUIDField(pk=True)
    season = fields.ForeignKeyField("models.Season", related_name="game_pieces")
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

class MatchScoutingField(Model):
    uuid = fields.UUIDField(pk=True)
    parent = fields.ForeignKeyField("models.MatchScoutingField", related_name="children", null=True)
    season = fields.ForeignKeyField("models.Season", related_name="fields")
    name = fields.CharField(max_length=255)
    field_type = fields.CharField(max_length=255) # section, string, large_number, small_number, boolean, choice, multiple_choice
    stat_type = fields.CharField(max_length=255) # section, auton_score, auton_miss, teleop_score, teleop_miss, capability, other, ignore
    game_piece = fields.ForeignKeyField("models.GamePiece", related_name="fields", null=True) # needed if stat_type is score or miss
    required = fields.BooleanField(default=False)
    options = fields.JSONField(null=True, default=list) # For integer maximum and minimums, choices, etc.
    order = fields.IntField(default=0) # The order the field should appear in the frontend or section
    organization = fields.ForeignKeyField("models.Organization", related_name="scouting_fields", null=True) # Optional, used if the field is specific to an organization
    created_at = fields.DatetimeField(auto_now_add=True)

class Event(Model):
    uuid = fields.UUIDField(pk=True)
    season = fields.ForeignKeyField("models.Season", related_name="events")
    event_code = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    type = fields.CharField(max_length=255)
    city = fields.CharField(max_length=255)
    country = fields.CharField(max_length=255)
    start_date = fields.DateField(null=True)
    end_date = fields.DateField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class MatchScoutingSubmission(Model):
    uuid = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="answers")
    event = fields.ForeignKeyField("models.Event", related_name="answers")
    team_number = fields.IntField(default=0)
    match_number = fields.IntField(default=0)
    match_type = fields.CharField(max_length=255, default="")
    created_at = fields.DatetimeField(auto_now_add=True)

class MatchScoutingAnswer(Model):
    uuid = fields.UUIDField(pk=True)
    field = fields.ForeignKeyField("models.MatchScoutingField", related_name="answers")
    value = fields.CharField(max_length=255, null=True)
    submission = fields.ForeignKeyField("models.MatchScoutingSubmission", related_name="answers")

#    Pit Scouting
# A PitScoutingField is defined in the admin interface
# When the pits list for a season and event is fetched, create it, and attempt to populate the teams in it from TBA
# Then the questions for that season (PitScoutingField) are loaded, and appear for each TeamPit
# New TeamPits can be created, and when an answer is added, create a PitScoutingAnswer
class PitScoutingField(Model):
    uuid = fields.UUIDField(pk=True)
    season = fields.ForeignKeyField("models.Season", related_name="pit_fields")
    name = fields.CharField(max_length=255)
    field_type = fields.CharField(max_length=255) # text, number, boolean, choice
    options = fields.JSONField(null=True, default=list) # For field_type=choice
    order = fields.IntField(default=0) # The order the field should appear in the frontend or section
    organization = fields.ForeignKeyField("models.Organization", related_name="pit_fields", null=True) # Optional, used if the field is specific to an organization
    created_at = fields.DatetimeField(auto_now_add=True)

class TeamPit(Model):
    uuid = fields.UUIDField(pk=True)
    team_number = fields.IntField()
    nickname = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    season = fields.ForeignKeyField("models.Season", related_name="team_pits")
    event = fields.ForeignKeyField("models.Event", related_name="team_pits")

class PitScoutingAnswer(Model):
    uuid = fields.UUIDField(pk=True)
    field = fields.ForeignKeyField("models.PitScoutingField", related_name="answers")
    value = fields.CharField(max_length=255, null=True)
    team = fields.ForeignKeyField("models.TeamPit", related_name="answers")
    username = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)