# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-11 03:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation_finance', '0018_auto_20170704_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_by',
            field=models.DateField(default=datetime.datetime(2017, 8, 5, 3, 20, 20, 483090)),
        ),
    ]
