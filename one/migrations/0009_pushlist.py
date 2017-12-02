# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0008_auto_20170910_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pushlist',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('bookname', models.TextField()),
                ('usermail', models.CharField(max_length=30)),
                ('bookpath', models.TextField()),
            ],
        ),
    ]
