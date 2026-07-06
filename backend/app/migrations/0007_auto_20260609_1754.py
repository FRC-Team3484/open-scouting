from tortoise import migrations
from tortoise.migrations import operations as ops
import functools
from json import dumps, loads
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0006_auto_20260609_1646')]

    initial = False

    operations = [
        ops.AlterField(
            model_name='Settings',
            name='favorite_events',
            field=fields.JSONField(null=True, default=list, description='The list of favorite events for the user', encoder=functools.partial(dumps, separators=(',', ':')), decoder=loads),
        ),
    ]
