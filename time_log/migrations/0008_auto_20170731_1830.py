# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-31 18:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('time_log', '0007_auto_20170731_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabilityforday',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL, verbose_name='Staff Member'),
        ),
    ]
