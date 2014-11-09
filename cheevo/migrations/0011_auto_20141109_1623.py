# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0010_steamgame_appid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steamuser',
            name='nickname',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(code='invalid_username', regex='([A-Za-z0-9\\-\\_]+)', message='Steam username can only consist of alphanumeric characters and underscores')]),
            preserve_default=True,
        ),
    ]
