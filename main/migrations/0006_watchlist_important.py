# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160225_0652'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='important',
            field=models.BooleanField(default=False),
        ),
    ]
