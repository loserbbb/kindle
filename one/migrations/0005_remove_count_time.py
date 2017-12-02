# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0004_count_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='count',
            name='time',
        ),
    ]
