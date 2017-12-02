# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0002_auto_20170910_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='fans',
            name='lastdownload',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='fans',
            name='downloademail',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fans',
            name='lastpush',
            field=models.DateField(null=True),
        ),
    ]
