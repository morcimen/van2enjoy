# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 11:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('van2enjoy_app', '0018_auto_20161021_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitios',
            name='provincia',
        ),
    ]
