# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0016_remove_steamgame_is_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='steamuser',
            name='personaname',
            field=models.CharField(default='0', max_length=255),
            preserve_default=True,
        ),
    ]
