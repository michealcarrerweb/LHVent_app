# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-25 01:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0002_auto_20170724_0150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='scheduled',
        ),
    ]
