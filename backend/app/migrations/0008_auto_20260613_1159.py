from tortoise import migrations
from tortoise.migrations import operations as ops
from ..setting_fields import ArraySetting

class Migration(migrations.Migration):
    dependencies = [('models', '0007_auto_20260609_1754')]

    initial = False

    operations = [
        ops.AlterField(
            model_name='Settings',
            name='favorite_events',
            field=ArraySetting(null=True, default=list, display_name='Favorite Events', setting_description='A list of favorite events for the user', section='General', visible=True),
        ),
    ]
