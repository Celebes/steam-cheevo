# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0009_remove_steamgame_appid'),
    ]

    operations = [
        migrations.AddField(
            model_name='steamgame',
            name='appid',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
