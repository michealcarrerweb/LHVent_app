# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-28 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_finance', '0005_auto_20170725_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicealteration',
            name='transaction_update',
            field=models.CharField(choices=[('Payment', 'Payment(-)'), ('Refund', 'Refund(+)'), ('Fee', 'Fee/Additional Cost(-)'), ('Discount', 'Discount(+)'), ('Error-Add', 'Add to previous entry amount due to             under error entry(-)'), ('Error-Off', 'Take from previous entry amount due             to over error entry(+)')], max_length=30),
        ),
    ]