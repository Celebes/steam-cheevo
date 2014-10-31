# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameAchievement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('unlocked', models.BooleanField(default=False)),
                ('percentage_of_people_that_unlocked', models.FloatField(default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SteamGame',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('hours_played', models.FloatField(default=0.0)),
                ('difficulty_score', models.FloatField(default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SteamUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nickname', models.CharField(max_length=255)),
                ('latest_refresh_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='steamgame',
            name='owner',
            field=models.ForeignKey(to='cheevo.SteamUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gameachievement',
            name='game',
            field=models.ForeignKey(to='cheevo.SteamGame'),
            preserve_default=True,
        ),
    ]
