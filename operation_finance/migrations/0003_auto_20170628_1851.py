# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-28 18:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation_finance', '0002_auto_20170628_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_by',
            field=models.DateField(default=datetime.datetime(2017, 7, 23, 18, 51, 11, 468579)),
        ),
    ]
