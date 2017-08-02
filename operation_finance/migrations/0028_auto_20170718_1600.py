# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-18 16:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation_finance', '0027_auto_20170718_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_by',
            field=models.DateField(default=datetime.datetime(2017, 8, 12, 16, 0, 45, 60516)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='slug',
            field=models.SlugField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='invoicealteration',
            name='slug',
            field=models.SlugField(blank=True, max_length=150),
        ),
    ]