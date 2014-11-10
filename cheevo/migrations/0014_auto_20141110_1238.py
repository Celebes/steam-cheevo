# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0013_auto_20141110_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steamuser',
            name='latest_refresh_date',
            field=models.DateTimeField(null=True, default=None, blank=True),
            preserve_default=True,
        ),
    ]
