# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-29 20:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation_finance', '0008_auto_20170629_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_by',
            field=models.DateField(default=datetime.datetime(2017, 7, 24, 20, 46, 22, 624505)),
        ),
    ]
