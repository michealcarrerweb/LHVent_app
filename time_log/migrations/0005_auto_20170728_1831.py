# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-28 18:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_log', '0004_auto_20170718_1645'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StaffLog',
            new_name='AvailabilityForDay',
        ),
        migrations.AlterUniqueTogether(
            name='daystafflogdetails',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='daystafflogdetails',
            name='day',
        ),
        migrations.RemoveField(
            model_name='daystafflogdetails',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='daystafflogentry',
            name='day',
        ),
        migrations.DeleteModel(
            name='DayLog',
        ),
        migrations.DeleteModel(
            name='DayStaffLogDetails',
        ),
        migrations.DeleteModel(
            name='DayStaffLogEntry',
        ),
    ]
