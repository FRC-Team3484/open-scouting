# Generated by Django 5.1.2 on 2024-12-04 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_event_custom_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='uuid',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
