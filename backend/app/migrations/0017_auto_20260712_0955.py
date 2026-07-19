from tortoise import migrations
from tortoise.migrations import operations as ops
import functools
from json import dumps, loads
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0016_auto_20260711_1127')]

    initial = False

    operations = [
        ops.CreateModel(
            name='Notification',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', db_constraint=True, to_field='uuid', related_name='notifications', on_delete=OnDelete.CASCADE)),
                ('title', fields.CharField(max_length=255)),
                ('message', fields.CharField(max_length=255)),
                ('type', fields.CharField(max_length=255)),
                ('action_type', fields.CharField(null=True, max_length=255)),
                ('action_data', fields.JSONField(null=True, default=dict, encoder=functools.partial(dumps, separators=(',', ':')), decoder=loads)),
                ('read', fields.BooleanField(default=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('created_by', fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL)),
            ],
            options={'table': 'notification', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Stores a notification for a user'},
            bases=['Model'],
        ),
    ]
