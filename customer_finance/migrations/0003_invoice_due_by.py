# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-20 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_finance', '0002_auto_20170718_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='due_by',
            field=models.DateField(blank=True, null=True),
        ),
    ]
