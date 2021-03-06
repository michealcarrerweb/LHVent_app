# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-24 01:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['origin', 'client']},
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_created',
        ),
        migrations.AddField(
            model_name='order',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='origin',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='slug',
            field=models.SlugField(blank=True, max_length=150),
        ),
    ]
