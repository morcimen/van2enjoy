# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('van2enjoy_app', '0022_delete_provincias'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provincias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provincia', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Provincias',
            },
        ),
    ]
