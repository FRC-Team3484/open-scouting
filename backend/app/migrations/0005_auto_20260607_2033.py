from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0004_auto_20260323_0916')]

    initial = False

    operations = [
        ops.CreateModel(
            name='Session',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('last_seen', fields.DatetimeField(auto_now=True, auto_now_add=False)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', null=True, db_constraint=True, to_field='uuid', related_name='sessions', on_delete=OnDelete.CASCADE)),
            ],
            options={'table': 'session', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a user session on the server'},
            bases=['Model'],
        ),
    ]
