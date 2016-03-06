# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('original_title', models.CharField(max_length=255)),
                ('tagline', models.CharField(max_length=255)),
                ('overview', models.TextField()),
                ('imdb_id', models.CharField(max_length=20)),
                ('release_date', models.DateField(null=True, blank=True)),
                ('original_language', models.CharField(max_length=20)),
                ('poster_path', models.CharField(max_length=100)),
                ('backdrop_path', models.CharField(max_length=100)),
                ('runtime', models.CharField(max_length=10)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
