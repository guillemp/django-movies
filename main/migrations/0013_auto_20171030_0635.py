# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='faff_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
