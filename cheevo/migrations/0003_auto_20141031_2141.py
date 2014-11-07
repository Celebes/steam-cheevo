# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0002_auto_20141031_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steamgame',
            name='owner',
        ),
        migrations.AddField(
            model_name='gameachievement',
            name='unlockers',
            field=models.ManyToManyField(to='cheevo.SteamUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='steamgame',
            name='owners',
            field=models.ManyToManyField(to='cheevo.SteamUser'),
            preserve_default=True,
        ),
    ]
