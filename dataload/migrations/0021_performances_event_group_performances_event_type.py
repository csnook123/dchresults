# Generated by Django 4.2.1 on 2023-06-14 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataload', '0020_athlete_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='performances',
            name='event_group',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='performances',
            name='event_type',
            field=models.CharField(default='', max_length=50),
        ),
    ]
