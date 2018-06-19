# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 16:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iati_codelists', '0006_add_budget_status_1'),
        ('iati', '0047_remove_multiple_documenttitles'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetSector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iati.Budget')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.Sector')),
            ],
        ),
    ]