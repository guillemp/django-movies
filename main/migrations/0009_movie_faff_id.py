# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20160306_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='faff_id',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
