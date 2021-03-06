# Generated by Django 3.1.5 on 2021-01-20 09:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.IntegerField(primary_key=True, serialize=False)),
                ('message', models.TextField(default='')),
                ('sent', models.DateTimeField(default=datetime.datetime(2021, 1, 20, 9, 32, 33, 485150, tzinfo=utc))),
                ('received', models.BooleanField(default=False)),
                ('message_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_from', to=settings.AUTH_USER_MODEL)),
                ('message_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
