# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 00:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_create',
            field=models.DateField(default=datetime.date(2017, 9, 30), verbose_name='Дата создания сообщения'),
        ),
        migrations.AlterField(
            model_name='section',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='date_create',
            field=models.DateField(default=datetime.date(2017, 9, 30), verbose_name='Дата создания темы'),
        ),
    ]
