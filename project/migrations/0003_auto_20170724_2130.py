# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-24 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20170724_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='worked',
            field=models.BooleanField(default=False, verbose_name='Обработано'),
        ),
    ]
