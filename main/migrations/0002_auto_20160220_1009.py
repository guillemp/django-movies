# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imdb_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_votes',
            field=models.IntegerField(default=0),
        ),
    ]
