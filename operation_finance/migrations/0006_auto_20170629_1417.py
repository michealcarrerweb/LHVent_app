# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-29 14:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation_finance', '0005_auto_20170628_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_by',
            field=models.DateField(default=datetime.datetime(2017, 7, 24, 14, 17, 2, 80987)),
        ),
    ]
