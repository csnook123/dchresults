# Generated by Django 4.2.1 on 2023-06-13 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dchcalendar', '0005_remove_event_test_event_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='Age_Group',
            field=models.CharField(blank=True, choices=[('1', 'Junior'), ('2', 'Senior'), ('3', 'Masters'), ('4', 'All')], help_text='Age Groups', max_length=32, null=True),
        ),
    ]
