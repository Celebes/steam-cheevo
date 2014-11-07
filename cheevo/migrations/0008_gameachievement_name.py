# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0007_auto_20141104_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameachievement',
            name='name',
            field=models.CharField(default='noname', max_length=255),
            preserve_default=True,
        ),
    ]
