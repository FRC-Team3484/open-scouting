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
    season = fields.ForeignKeyField("models.Season", related_name="fields")
    name = fields.CharField(max_length=255)
    field_type = fields.CharField(max_length=255) # string, large_number, small_number, boolean, choice, multiple_choice
    stat_type = fields.CharField(max_length=255) # auton_score, auton_miss, teleop_score, teleop_miss, capability, other, ignore
    game_piece = fields.ForeignKeyField("models.GamePiece", related_name="fields", null=True) # needed if stat_type is score or miss
    required = fields.BooleanField(default=False)
    options = fields.JSONField(null=True, default=list) # For integer maximum and minimums, choices, etc.
    order = fields.IntField(default=0) # The order the field should appear in the frontend or section
    organization = fields.ForeignKeyField("models.Organization", related_name="scouting_fields", null=True) # Optional, used if the field is specific to an organization
    created_at = fields.DatetimeField(auto_now_add=True)

class MatchScoutingSection(Model):
    uuid = fields.UUIDField(pk=True)
    season = fields.ForeignKeyField("models.Season", related_name="sections")
    name = fields.CharField(max_length=255)
    order = fields.IntField(default=0) # The order the section should appear in the frontend
    scouting_fields = fields.ManyToManyField("models.MatchScoutingField", related_name="sections") # The fields in the section
    organization = fields.ForeignKeyField("models.Organization", related_name="scouting_sections", null=True) # Optional, used if the section is specific to an organization
    created_at = fields.DatetimeField(auto_now_add=True)