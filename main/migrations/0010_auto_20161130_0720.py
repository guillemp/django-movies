# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_movie_faff_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='faff_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='faff_votes',
            field=models.IntegerField(default=0),
        ),
    ]
