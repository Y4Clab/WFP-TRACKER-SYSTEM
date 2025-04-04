# Generated by Django 5.0.6 on 2025-03-23 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_track', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('suspended', 'Suspended')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='mission',
            name='status',
            field=models.CharField(choices=[('planned', 'Planned'), ('completed', 'Completed'), ('active', 'Active')], max_length=50),
        ),
    ]
