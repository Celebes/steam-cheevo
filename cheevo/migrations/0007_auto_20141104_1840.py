# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0006_steamgame_is_game'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalStats',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('last_database_update', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='gameachievement',
            name='name',
        ),
        migrations.RemoveField(
            model_name='gameachievement',
            name='unlocked',
        ),
        migrations.RemoveField(
            model_name='gameachievement',
            name='unlockers',
        ),
        migrations.RemoveField(
            model_name='steamgame',
            name='hours_played',
        ),
    ]
