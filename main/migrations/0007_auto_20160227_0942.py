# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_watchlist_important'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blocklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('movie', models.ForeignKey(to='main.Movie')),
                ('user', models.ForeignKey(related_name='blocklist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='blocklist',
            unique_together=set([('user', 'movie')]),
        ),
    ]
