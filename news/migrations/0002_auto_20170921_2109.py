# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-21 21:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date_pub',
            field=models.DateField(default=datetime.date(2017, 9, 21)),
        ),
    ]
