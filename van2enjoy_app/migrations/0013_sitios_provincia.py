# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 00:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('van2enjoy_app', '0012_remove_sitios_provincia'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitios',
            name='provincia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='van2enjoy_app.Provincias'),
        ),
    ]
