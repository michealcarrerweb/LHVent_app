# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-01 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_log', '0010_auto_20170801_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='stafflogdetailsforday',
            name='scheduled_end',
            field=models.TimeField(blank=True, null=True, verbose_name='actual start'),
        ),
        migrations.AddField(
            model_name='stafflogdetailsforday',
            name='scheduled_start',
            field=models.TimeField(blank=True, null=True, verbose_name='actual start'),
        ),
    ]
