# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20161130_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='backdrop_path',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imdb_id',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='original_language',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='original_title',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='overview',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster_path',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='runtime',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='tagline',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
