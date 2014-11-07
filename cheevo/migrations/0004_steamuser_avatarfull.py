# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheevo', '0003_auto_20141031_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='steamuser',
            name='avatarfull',
            field=models.CharField(max_length=255, default='0'),
            preserve_default=True,
        ),
    ]
