# Generated by Django 3.1.5 on 2021-01-20 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tournament', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('match_id', models.IntegerField(primary_key=True, serialize=False)),
                ('score', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('round', models.IntegerField(blank=True, null=True)),
                ('opponents', models.ManyToManyField(related_name='opponents', to=settings.AUTH_USER_MODEL)),
                ('players', models.ManyToManyField(related_name='players', to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.tournament')),
            ],
        ),
    ]
