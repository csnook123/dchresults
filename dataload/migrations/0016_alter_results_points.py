# Generated by Django 4.2.1 on 2023-05-26 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataload', '0015_results_event_age_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
