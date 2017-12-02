# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activationcode',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(unique=True, max_length=32)),
                ('rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='fans',
            name='deadline',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='fans',
            name='downloademail',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='fans',
            name='downloadtimes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='fans',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='bookname',
            field=models.CharField(max_length=50),
        ),
    ]
