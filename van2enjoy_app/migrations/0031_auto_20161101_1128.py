# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 11:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('van2enjoy_app', '0030_auto_20161030_2328'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitios',
            old_name='baños',
            new_name='servicios',
        ),
    ]
