# Generated by Django 5.0.6 on 2025-04-06 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_track', '0011_rename_unique_id_mission_mission_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='truck',
            name='plate_number',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
