# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-20 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation_finance', '0031_auto_20170718_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_by',
            field=models.DateField(blank=True, null=True),
        ),
    ]