from tortoise import migrations
from tortoise.migrations import operations as ops
import functools
from json import dumps, loads
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='Organization',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('name', fields.CharField(max_length=255)),
                ('description', fields.TextField(null=True, unique=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'organization', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines an organization on the server, which is used to offer custom '},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Season',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('year', fields.IntField()),
                ('name', fields.CharField(max_length=255)),
                ('active', fields.BooleanField(default=True)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'season', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a season on the server. One season should be created for each individual FRC game'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Event',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('season', fields.ForeignKeyField('models.Season', source_field='season_id', db_constraint=True, to_field='uuid', related_name='events', on_delete=OnDelete.CASCADE)),
                ('event_code', fields.CharField(max_length=255)),
                ('name', fields.CharField(max_length=255)),
                ('type', fields.CharField(max_length=255)),
                ('city', fields.CharField(max_length=255)),
                ('country', fields.CharField(max_length=255)),
                ('start_date', fields.DateField(null=True)),
                ('end_date', fields.DateField(null=True)),
                ('pits_generated', fields.BooleanField(default=False)),
                ('custom', fields.BooleanField(default=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'event', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a single event on the server'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='GamePiece',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('season', fields.ForeignKeyField('models.Season', source_field='season_id', db_constraint=True, to_field='uuid', related_name='game_pieces', on_delete=OnDelete.CASCADE)),
                ('name', fields.CharField(max_length=255)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'gamepiece', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a game piece on the server, which is used to specify the game piece used in a field'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='MatchScoutingField',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('parent', fields.ForeignKeyField('models.MatchScoutingField', source_field='parent_id', null=True, db_constraint=True, to_field='uuid', related_name='children', on_delete=OnDelete.CASCADE)),
                ('season', fields.ForeignKeyField('models.Season', source_field='season_id', db_constraint=True, to_field='uuid', related_name='fields', on_delete=OnDelete.CASCADE)),
                ('name', fields.CharField(max_length=255)),
                ('description', fields.TextField(null=True, unique=False)),
                ('field_type', fields.CharField(max_length=255)),
                ('stat_type', fields.CharField(max_length=255)),
                ('game_piece', fields.ForeignKeyField('models.GamePiece', source_field='game_piece_id', null=True, db_constraint=True, to_field='uuid', related_name='fields', on_delete=OnDelete.CASCADE)),
                ('required', fields.BooleanField(default=False)),
                ('options', fields.JSONField(null=True, default=list, encoder=functools.partial(dumps, separators=(',', ':')), decoder=loads)),
                ('order', fields.IntField(default=0)),
                ('organization', fields.ForeignKeyField('models.Organization', source_field='organization_id', null=True, db_constraint=True, to_field='uuid', related_name='scouting_fields', on_delete=OnDelete.CASCADE)),
                ('archived', fields.BooleanField(default=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'matchscoutingfield', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a single question that should be asked when match scouting for a season'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='PitScoutingField',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('season', fields.ForeignKeyField('models.Season', source_field='season_id', db_constraint=True, to_field='uuid', related_name='pit_fields', on_delete=OnDelete.CASCADE)),
                ('name', fields.CharField(max_length=255)),
                ('description', fields.TextField(null=True, unique=False)),
                ('field_type', fields.CharField(max_length=255)),
                ('options', fields.JSONField(null=True, default=list, encoder=functools.partial(dumps, separators=(',', ':')), decoder=loads)),
                ('order', fields.IntField(default=0)),
                ('organization', fields.ForeignKeyField('models.Organization', source_field='organization_id', null=True, db_constraint=True, to_field='uuid', related_name='pit_fields', on_delete=OnDelete.CASCADE)),
                ('archived', fields.BooleanField(default=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'pitscoutingfield', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a single question that should be asked when pit scouting for a season'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='TeamPit',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('team_number', fields.IntField()),
                ('nickname', fields.CharField(max_length=255)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('season', fields.ForeignKeyField('models.Season', source_field='season_id', db_constraint=True, to_field='uuid', related_name='team_pits', on_delete=OnDelete.CASCADE)),
                ('event', fields.ForeignKeyField('models.Event', source_field='event_id', db_constraint=True, to_field='uuid', related_name='team_pits', on_delete=OnDelete.CASCADE)),
            ],
            options={'table': 'teampit', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a pit for a single team, per event per season'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='PitScoutingAnswer',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('field', fields.ForeignKeyField('models.PitScoutingField', source_field='field_id', db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.CASCADE)),
                ('value', fields.CharField(null=True, max_length=255)),
                ('team', fields.ForeignKeyField('models.TeamPit', source_field='team_id', db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.CASCADE)),
                ('username', fields.CharField(null=True, max_length=255)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'pitscoutinganswer', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a single pit scouting answer for a pit scouting field. These belong to a TeamPit'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='User',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('username', fields.CharField(unique=True, max_length=255)),
                ('email', fields.CharField(unique=True, max_length=255)),
                ('hashed_password', fields.CharField(max_length=255)),
                ('is_superuser', fields.BooleanField(default=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'user', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a unique user account on the server'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='MatchScoutingSubmission',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.CASCADE)),
                ('event', fields.ForeignKeyField('models.Event', source_field='event_id', db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.CASCADE)),
                ('team_number', fields.IntField(default=0)),
                ('match_number', fields.IntField(default=0)),
                ('match_type', fields.CharField(default='', max_length=255)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'matchscoutingsubmission', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a single match scouting submission on the server. This includes the match number'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='MatchScoutingAnswer',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('field', fields.ForeignKeyField('models.MatchScoutingField', source_field='field_id', db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.CASCADE)),
                ('value', fields.CharField(null=True, max_length=255)),
                ('submission', fields.ForeignKeyField('models.MatchScoutingSubmission', source_field='submission_id', db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.CASCADE)),
            ],
            options={'table': 'matchscoutinganswer', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a single match scouting answer for a field. These belong to a MatchScoutingSubmission'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='OrganizationMember',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('organization', fields.ForeignKeyField('models.Organization', source_field='organization_id', db_constraint=True, to_field='uuid', related_name='members', on_delete=OnDelete.CASCADE)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', db_constraint=True, to_field='uuid', related_name='organizations', on_delete=OnDelete.CASCADE)),
                ('role', fields.CharField(max_length=255)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'organizationmember', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a member of an organization, and their role within the organization'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Profile',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', db_constraint=True, to_field='uuid', related_name='profiles', on_delete=OnDelete.CASCADE)),
                ('display_name', fields.CharField(max_length=255)),
                ('team_number', fields.IntField(null=True)),
            ],
            options={'table': 'profile', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a profile for a user, with cosmetic information not required for basic use on the server'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Settings',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', db_constraint=True, to_field='uuid', related_name='settings', on_delete=OnDelete.CASCADE)),
                ('favorite_events', fields.JSONField(null=True, default=list, encoder=functools.partial(dumps, separators=(',', ':')), decoder=loads)),
            ],
            options={'table': 'settings', 'app': 'models', 'pk_attr': 'uuid', 'table_description': "Defines a user's settings on the server"},
            bases=['Model'],
        ),
    ]
