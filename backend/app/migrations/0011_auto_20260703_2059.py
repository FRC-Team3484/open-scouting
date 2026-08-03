from tortoise import migrations
from tortoise.migrations import operations as ops
import functools
from json import dumps, loads
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0010_auto_20260617_1955')]

    initial = False

    operations = [
        ops.CreateModel(
            name='Passkey',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', db_constraint=True, to_field='uuid', related_name='passkeys', on_delete=OnDelete.CASCADE)),
                ('credential_id', fields.BinaryField()),
                ('public_key', fields.BinaryField()),
                ('sign_count', fields.BigIntField(default=0)),
                ('transports', fields.JSONField(null=True, encoder=functools.partial(dumps, separators=(',', ':')), decoder=loads)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'passkey', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a passkey for a user, used to log them in'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='WebAuthnChallenge',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('challenge', fields.CharField(unique=True, max_length=255)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', null=True, db_constraint=True, to_field='uuid', related_name='webauthn_challenges', on_delete=OnDelete.CASCADE)),
                ('expires_at', fields.DatetimeField(auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'webauthnchallenge', 'app': 'models', 'pk_attr': 'uuid'},
            bases=['Model'],
        ),
    ]
