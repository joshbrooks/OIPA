# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 00:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iati_synchroniser', '0006_datasetnote_variable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetnote',
            name='variable',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
