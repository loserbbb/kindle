# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0005_remove_count_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='count',
            name='time',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
    ]
