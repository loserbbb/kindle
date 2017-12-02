# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0003_auto_20170910_0257'),
    ]

    operations = [
        migrations.AddField(
            model_name='count',
            name='time',
            field=models.DateTimeField(null=True, auto_now_add=True),
            preserve_default=False,
        ),
    ]
