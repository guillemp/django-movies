# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20160227_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieCast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('movie', models.ForeignKey(to='main.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('profile_path', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='moviecast',
            name='person',
            field=models.ForeignKey(to='main.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='cast',
            field=models.ManyToManyField(related_name='movies', through='main.MovieCast', to='main.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='moviecast',
            unique_together=set([('person', 'movie')]),
        ),
    ]
