# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-12 12:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation_finance', '0022_auto_20170712_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_by',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 12, 13, 18, 184542)),
        ),
    ]