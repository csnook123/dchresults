# Generated by Django 4.2.1 on 2023-05-29 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataload', '0019_alter_performances_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
