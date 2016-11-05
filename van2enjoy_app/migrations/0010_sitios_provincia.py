# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 23:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('van2enjoy_app', '0009_remove_sitios_provincia'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitios',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='van2enjoy_app.Provincias'),
            preserve_default=False,
        ),
    ]
