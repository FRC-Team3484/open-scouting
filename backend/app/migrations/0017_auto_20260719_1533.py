from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0016_auto_20260711_1127')]

    initial = False

    operations = [
        ops.CreateModel(
            name='Report',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('type', fields.CharField(max_length=255)),
                ('content_uuid', fields.UUIDField()),
                ('report_reason', fields.CharField(max_length=255)),
                ('report_details', fields.TextField(null=True, unique=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('created_by', fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL)),
            ],
            options={'table': 'report', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'A model for user-defined reports of content. Superusers can view these reports in the admin panel, and remove content as needed.'},
            bases=['Model'],
        ),
    ]
