from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0008_auto_20260613_1159')]

    initial = False

    operations = [
        ops.AddField(
            model_name='Profile',
            name='profile_picture_url',
            field=fields.CharField(null=True, max_length=255),
        ),
    ]
