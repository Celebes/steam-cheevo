# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0005_steamgame_has_achievements'),
    ]

    operations = [
        migrations.AddField(
            model_name='steamgame',
            name='is_game',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
