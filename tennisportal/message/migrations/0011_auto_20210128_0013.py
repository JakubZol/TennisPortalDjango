# Generated by Django 3.1.5 on 2021-01-28 00:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0010_auto_20210128_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 28, 0, 13, 50, 239911, tzinfo=utc)),
        ),
    ]