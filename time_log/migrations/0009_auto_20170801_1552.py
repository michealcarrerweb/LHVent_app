# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-01 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_log', '0008_auto_20170731_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabilityforday',
            name='day',
            field=models.CharField(max_length=12, verbose_name='Day of the week'),
        ),
    ]
