# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0007_accesskey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesskey',
            name='gettime',
            field=models.IntegerField(),
        ),
    ]
