from typing import Any, override
from uuid import uuid5

from tortoise import fields
from tortoise.models import Model

from .setting_fields import ArraySetting, BooleanSetting, JSONSetting, NumberSetting, StringSetting

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
        created_by (Session): The session that created the user
    """
    uuid = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_superuser = fields.BooleanField(default=False)
    email_verified = fields.BooleanField(default=False, db_default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

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
        profile_picture_url (str): The URL of the profile picture of the user
        created_at (datetime): The date and time the profile was created
        created_by (Session): The session that created the profile
    """
    uuid = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="profiles", on_delete=fields.CASCADE)
    display_name = fields.CharField(max_length=255)
    team_number = fields.IntField(null=True)
    profile_picture_url = fields.CharField(max_length=255, null=True, default=None)

    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

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
        created_by (Session): The session that created the organization
    """
    uuid = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

class OrganizationMember(Model):
    """
    Defines a member of an organization, and their role within the organization

    Attributes:
        uuid (UUID): The unique identifier for the organization member
        organization (Organization): The organization the member is a member of
        user (User): The user the member is a member of
        role (str): The role of the member in the organization
        created_at (datetime): The date and time the organization member was created
        created_by (Session): The session that created the organization member
    """
    uuid = fields.UUIDField(pk=True)
    organization = fields.ForeignKeyField("models.Organization", related_name="members", on_delete=fields.CASCADE)
    user = fields.ForeignKeyField("models.User", related_name="organizations", on_delete=fields.CASCADE)
    role = fields.CharField(max_length=255) # member, admin

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

class Settings(Model):
    """
    Defines a user's settings on the server

    Each setting is a database field, and should have a default value. 
        These settings do not need to be hardcoded anywhere, other than accessing them in the frontend

    Attributes:
        uuid (UUID): The unique identifier for the settings
        user (User): The user the settings are associated with
        created_at (datetime): The date and time the settings were created
        created_by (Session): The session that created the settings
        favorite_events (list): The list of favorite events for the user
    """
    uuid = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="settings", on_delete=fields.CASCADE)

    created_at = fields.DatetimeField(auto_now_add=True, null=True) # This field was not added until v2.2.0, so it may be null in prod
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

    # Settings:
    favorite_events = ArraySetting(null=True, default=list, display_name="Favorite Events", setting_description="Your favorite events, which appear at the top of the event list", section="General", visible=True)

class Session(Model):
    """
    Defines a user session on the server

    Will be used to keep track of related actions on the server, for moderation purposes.
        No personal information will ever be stored, it will only be used to be tied to database actions

    Attributes:
        uuid (UUID): The unique identifier for the session
        created_at (datetime): The date and time the session was created
        last_seen (datetime): The date and time the session was last seen
        user (User): The user the session is associated with
    """
    uuid = fields.UUIDField(pk=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    last_seen = fields.DatetimeField(auto_now=True)

    user = fields.ForeignKeyField(
        "models.User", 
        related_name="sessions",
        null=True,
        on_delete=fields.SET_NULL
    )

class VerificationCode(Model):
    """
    Defines a verification code for a user, used to verify their email or change their password

    Attributes:
        uuid (UUID): The unique identifier for the verification code
        user (User): The user the verification code is associated with
        code (str): The verification code
        email (str): The email the verification code is associated with
        verified (bool): Whether the verification code has been verified
        created_at (datetime): The date and time the verification code was created
        created_by (Session): The session that created the verification code
    """
    uuid = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="verification_codes", null=True, on_delete=fields.CASCADE)
    code = fields.CharField(max_length=6)
    email = fields.CharField(max_length=255)
    verified = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

class Passkey(Model):
    """
    Defines a passkey for a user, used to log them in

    Attributes:
        uuid (UUID): The unique identifier for the passkey
        user (User): The user the passkey is associated with
        credential_id (bytes): The credential id of the passkey
        public_key (bytes): The public key of the passkey
        sign_count (int): The sign count of the passkey
        transports (list): The transports of the passkey
        created_at (datetime): The date and time the passkey was created
        created_by (Session): The session that created the passkey
    """
    uuid = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="passkeys",
        on_delete=fields.CASCADE
    )
    label = fields.CharField(max_length=255, null=True)

    credential_id = fields.BinaryField()
    public_key = fields.BinaryField()
    sign_count = fields.BigIntField(default=0)
    transports = fields.JSONField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

class WebAuthnChallenge(Model):
    """
    Store a webauthn challenge for a user

    Attributes:
        uuid (UUID): The unique identifier for the challenge
        challenge (bytes): The challenge
        user (User): The user the challenge is associated with
        expires_at (datetime): The date and time the challenge expires
        created_at (datetime): The date and time the challenge was created
        created_by (Session): The session that created the challenge
    """
    uuid = fields.UUIDField(pk=True)
    challenge = fields.BinaryField(null=True)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="webauthn_challenges",
        null=True,
        on_delete=fields.CASCADE
    )
    expires_at = fields.DatetimeField()

    created_at = fields.DatetimeField(auto_now_add=True, null=True) # This field was not added until v2.2.0, so it may be null in prod
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

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
        created_by (Session): The session that created the season
    """
    uuid = fields.UUIDField(pk=True)
    year = fields.IntField()
    name = fields.CharField(max_length=255)
    active = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

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
        created_by (Session): The session that created the game piece
    """
    uuid = fields.UUIDField(pk=True)
    season = fields.ForeignKeyField("models.Season", related_name="game_pieces", null=True, on_delete=fields.SET_NULL)
    name = fields.CharField(max_length=255)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

class MatchScoutingField(Model):
    """
    Defines a single question that should be asked when match scouting for a season

    Attributes:
        uuid (UUID): The unique identifier for the match scouting field
        parent (MatchScoutingField): The parent of the match scouting field
        season (Season): The season the match scouting field is associated with
        name (str): The name of the match scouting field
        description (str): The description of the match scouting field
        field_type (str): The type of the match scouting field
        stat_type (str): The stat type of the match scouting field
        game_piece (GamePiece): The game piece used in the match scouting field
        required (bool): Whether the match scouting field is required or not
        options (list): The options for the match scouting field
        order (int): The order of the match scouting field
        organization (Organization): The organization the match scouting field is associated with
        archived (bool): Whether the match scouting field is archived or not
        created_at (datetime): The date and time the match scouting field was created
        created_by (Session): The session that created the match scouting field
    """
    uuid = fields.UUIDField(pk=True)
    parent = fields.ForeignKeyField("models.MatchScoutingField", related_name="children", null=True, on_delete=fields.SET_NULL)
    season = fields.ForeignKeyField("models.Season", related_name="fields", null=True, on_delete=fields.SET_NULL)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    field_type = fields.CharField(max_length=255) # section, string, large_number, small_number, boolean, choice, multiple_choice
    stat_type = fields.CharField(max_length=255) # section, auton_score, auton_miss, teleop_score, teleop_miss, capability, other, ignore
    game_piece = fields.ForeignKeyField("models.GamePiece", related_name="fields", null=True, on_delete=fields.SET_NULL) # needed if stat_type is score or miss
    required = fields.BooleanField(default=False)
    options = fields.JSONField(null=True, default=dict) # For integer maximum and minimums, choices, etc.
    order = fields.IntField(default=0) # The order the field should appear in the frontend or section
    organization = fields.ForeignKeyField("models.Organization", related_name="scouting_fields", null=True, on_delete=fields.CASCADE) # Optional, used if the field is specific to an organization
    archived= fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

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
        created_by (Session): The session that created the event
    """
    uuid = fields.UUIDField(pk=True)
    season = fields.ForeignKeyField("models.Season", related_name="events", null=True, on_delete=fields.SET_NULL)
    event_code = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    type = fields.CharField(max_length=255)
    city = fields.CharField(max_length=255)
    country = fields.CharField(max_length=255)
    start_date = fields.DateField(null=True)
    end_date = fields.DateField(null=True)
    pits_generated = fields.BooleanField(default=False)
    custom = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

class MatchScoutingSubmission(Model):
    """
    Defines a single match scouting submission on the server. This includes the match number
        and team number, and is a single scouting report made up of several answers for the individual fields

    Attributes:
        uuid (UUID): The unique identifier for the match scouting submission
        event (Event): The event the match scouting submission is associated with
        team_number (int): The team number of the match scouting submission
        match_number (int): The match number of the match scouting submission
        match_type (str): The match type of the match scouting submission
        created_at (datetime): The date and time the match scouting submission was created
        created_by (Session): The session that created the match scouting submission
    """
    uuid = fields.UUIDField(pk=True)
    event = fields.ForeignKeyField("models.Event", related_name="answers", null=True, on_delete=fields.SET_NULL)
    team_number = fields.IntField(default=0)
    match_number = fields.IntField(default=0)
    match_type = fields.CharField(max_length=255, default="")

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

class MatchScoutingAnswer(Model):
    """
    Defines a single match scouting answer for a field. These belong to a MatchScoutingSubmission

    Attributes:
        uuid (UUID): The unique identifier for the match scouting answer
        field (MatchScoutingField): The field the match scouting answer is associated with
        value (str): The value of the match scouting answer
        submission (MatchScoutingSubmission): The match scouting submission the match scouting answer is associated with
        created_at (datetime): The date and time the match scouting answer was created
        created_by (Session): The session that created the match scouting answer
    """
    uuid = fields.UUIDField(pk=True)
    field = fields.ForeignKeyField("models.MatchScoutingField", related_name="answers", null=True, on_delete=fields.SET_NULL)
    value = fields.CharField(max_length=255, null=True)
    submission = fields.ForeignKeyField("models.MatchScoutingSubmission", related_name="answers", null=True, on_delete=fields.SET_NULL)

    created_at = fields.DatetimeField(auto_now_add=True, null=True) # This field was not added until v2.2.0, so it may be null in prod
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

#    Pit Scouting
class PitScoutingField(Model):
    """
    Defines a single question that should be asked when pit scouting for a season

    Attributes:
        uuid (UUID): The unique identifier for the pit scouting field
        season (Season): The season the pit scouting field is associated with
        name (str): The name of the pit scouting field
        description (str): The description of the pit scouting field
        required (bool): Whether the pit scouting field is required or not
        field_type (str): The type of the pit scouting field
        options (list): The options for the pit scouting field
        order (int): The order of the pit scouting field
        organization (Organization): The organization the pit scouting field is associated with
        archived (bool): Whether the pit scouting field is archived or not
        created_at (datetime): The date and time the pit scouting field was created
        created_by (Session): The session that created the pit scouting field
    """
    uuid = fields.UUIDField(pk=True)
    season = fields.ForeignKeyField("models.Season", related_name="pit_fields", null=True, on_delete=fields.SET_NULL)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    required = fields.BooleanField(default=False)
    field_type = fields.CharField(max_length=255) # text, number, boolean, choice
    options = fields.JSONField(null=True, default=list) # For field_type=choice
    order = fields.IntField(default=0) # The order the field should appear in the frontend or section
    organization = fields.ForeignKeyField("models.Organization", related_name="pit_fields", null=True, on_delete=fields.CASCADE) # Optional, used if the field is specific to an organization
    archived= fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

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
        created_at (datetime): The date and time the team pit was created
        created_by (Session): The session that created the team pit
    """
    uuid = fields.UUIDField(pk=True)
    team_number = fields.IntField()
    nickname = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    season = fields.ForeignKeyField("models.Season", related_name="team_pits", null=True, on_delete=fields.SET_NULL)
    event = fields.ForeignKeyField("models.Event", related_name="team_pits", null=True, on_delete=fields.SET_NULL)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

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
        created_by (Session): The session that created the pit scouting answer
    """
    uuid = fields.UUIDField(pk=True)
    field = fields.ForeignKeyField("models.PitScoutingField", related_name="answers", null=True, on_delete=fields.SET_NULL)
    value = fields.CharField(max_length=255, null=True)
    team = fields.ForeignKeyField("models.TeamPit", related_name="answers", null=True, on_delete=fields.SET_NULL)
    username = fields.CharField(max_length=255, null=True) # TODO: Remove in favor of created_by

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)

# Reports
class Report(Model):
    """
    A model for user-defined reports of content. Superusers can view these reports in the admin panel, and remove content as needed.

    MatchScoutingSubmissions, MatchScoutingAnswers, TeamPits, PitScoutingAnswers, and Events where custom=True can be reported

    Attributes:
        uuid (UUID): The unique identifier for the report
        type (str): The type of content being reported
        content_uuid (UUID): The UUID of the content being reported
        report_reason (str): The reason for reporting the content
        report_details (str): Additional details about the report
        created_at (datetime): The date and time the report was created
        created_by (Session): The session that created the report
    """
    uuid = fields.UUIDField(pk=True)
    type = fields.CharField(max_length=255) # match_scouting_submission, match_scouting_answer, team_pit, pit_scouting_answer, event
    content_uuid = fields.UUIDField()
    report_reason = fields.CharField(max_length=255) # spam, inaccurate, inappropriate, offensive, duplicate, other
    report_details = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.ForeignKeyField("models.Session", related_name=False, null=True, on_delete=fields.SET_NULL)