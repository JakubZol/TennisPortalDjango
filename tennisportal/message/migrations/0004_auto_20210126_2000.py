# Generated by Django 3.1.5 on 2021-01-26 20:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_auto_20210126_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 26, 20, 0, 56, 422827, tzinfo=utc)),
        ),
    ]
