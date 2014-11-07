# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0008_gameachievement_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steamgame',
            name='appid',
        ),
    ]
