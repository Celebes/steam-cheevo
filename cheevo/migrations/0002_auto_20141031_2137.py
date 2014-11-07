# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='steamgame',
            name='appid',
            field=models.CharField(max_length=50, default='0'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='steamgame',
            name='img_icon_url',
            field=models.CharField(max_length=255, default='0'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='steamuser',
            name='steam_id',
            field=models.CharField(max_length=50, default='0'),
            preserve_default=True,
        ),
    ]
