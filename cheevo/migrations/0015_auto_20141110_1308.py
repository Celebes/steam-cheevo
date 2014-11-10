# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0014_auto_20141110_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='steamgame',
            name='below_one_ach_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='steamgame',
            name='min_achievement',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
