# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0004_steamuser_avatarfull'),
    ]

    operations = [
        migrations.AddField(
            model_name='steamgame',
            name='has_achievements',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
