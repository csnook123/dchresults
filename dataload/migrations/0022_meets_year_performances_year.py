# Generated by Django 4.2.1 on 2023-06-14 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataload', '0021_performances_event_group_performances_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='meets',
            name='year',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='performances',
            name='year',
            field=models.CharField(default='', max_length=50),
        ),
    ]
