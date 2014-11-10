# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0015_auto_20141110_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steamgame',
            name='is_game',
        ),
    ]
