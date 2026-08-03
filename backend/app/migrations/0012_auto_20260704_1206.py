from tortoise import migrations
from tortoise.migrations import operations as ops

class Migration(migrations.Migration):
    dependencies = [('models', '0011_auto_20260703_2059')]

    initial = False

    operations = [
        ops.RemoveField(model_name='WebAuthnChallenge', name='challenge'),
    ]
