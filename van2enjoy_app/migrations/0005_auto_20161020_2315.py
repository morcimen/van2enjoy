# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 23:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('van2enjoy_app', '0004_auto_20161020_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitios',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
