# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0011_auto_20141109_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steamuser',
            name='latest_refresh_date',
            field=models.DateTimeField(default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='steamuser',
            name='nickname',
            field=models.CharField(validators=[django.core.validators.RegexValidator(code='invalid_username', message='Steam username can only consist of alphanumeric characters and underscores', regex='^[A-Za-z0-9\\_]+$')], max_length=255),
            preserve_default=True,
        ),
    ]
