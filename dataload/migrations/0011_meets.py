# Generated by Django 4.2.1 on 2023-05-26 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataload', '0010_performances_age_group_performance'),
    ]

    operations = [
        migrations.CreateModel(
            name='meets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(default='', max_length=50)),
                ('meeting', models.CharField(default='', max_length=50)),
                ('venue', models.CharField(default='', max_length=50)),
                ('type', models.CharField(default='', max_length=50)),
                ('meeting_id', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
