# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0006_count_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accesskey',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('key', models.TextField()),
                ('gettime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
