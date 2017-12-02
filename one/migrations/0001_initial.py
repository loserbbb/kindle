# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('bookpath', models.TextField()),
                ('bookname', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Fans',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fansid', models.CharField(unique=True, max_length=35)),
                ('email', models.CharField(max_length=30)),
                ('lastpush', models.DateField(auto_now=True)),
                ('times', models.IntegerField(default=0)),
            ],
        ),
    ]
