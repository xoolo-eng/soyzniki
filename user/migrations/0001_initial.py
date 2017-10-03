# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 23:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('soyzniki', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Secret',
            fields=[
                ('id', models.BigAutoField(max_length=21, primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(verbose_name='id зарегестрированного пользователя')),
                ('sol', models.CharField(max_length=20, verbose_name='соль для хеширования')),
                ('shadow_id', models.CharField(max_length=20, verbose_name='паралельный id пользователя')),
                ('hash_passwd', models.TextField(verbose_name='хеш пароля')),
            ],
            options={
                'db_table': 'info',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(max_length=21, primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=255, verbose_name='Логин / Login')),
                ('name', models.CharField(max_length=50, verbose_name='Собственное имя')),
                ('family', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('telephone', models.CharField(max_length=25, verbose_name='Телефон')),
                ('street', models.CharField(max_length=150, verbose_name='Улица проживания')),
                ('hash_passwd', models.TextField(verbose_name='хеш пароля')),
                ('activate', models.BooleanField(verbose_name='Проверенный email')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soyzniki.City', verbose_name='Населенный пункт проживания')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soyzniki.Country', verbose_name='Страна проживания')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soyzniki.District', verbose_name='Район проживания')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soyzniki.Region', verbose_name='Регион / Область проживания')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'users',
            },
        ),
    ]
