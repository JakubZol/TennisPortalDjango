# Generated by Django 3.1.5 on 2021-01-26 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0004_tournament_rounds_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='rounds_number',
            field=models.IntegerField(),
        ),
    ]
