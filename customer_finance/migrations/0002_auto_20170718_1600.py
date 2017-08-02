# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-18 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerconflict',
            name='slug',
            field=models.SlugField(blank=True, max_length=150),
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
        migrations.AlterField(
            model_name='pricequote',
            name='slug',
            field=models.SlugField(blank=True, max_length=150),
        ),
    ]
