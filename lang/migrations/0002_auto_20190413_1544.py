# Generated by Django 2.2 on 2019-04-13 15:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lang', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlearnslanguage',
            name='started_learning',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 13, 15, 44, 27, 850642, tzinfo=utc)),
        ),
    ]