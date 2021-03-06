# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-30 12:27
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20170416_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='alt_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=15, null=True, verbose_name='alternate phone (not required)'),
        ),
        migrations.AddField(
            model_name='account',
            name='city',
            field=models.CharField(blank=True, help_text='example: Allentown', max_length=100, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='account',
            name='initial_password',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='main_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=15, verbose_name='main phone'),
        ),
        migrations.AddField(
            model_name='account',
            name='spouse_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='spouse name'),
        ),
        migrations.AddField(
            model_name='account',
            name='state',
            field=models.CharField(choices=[('PA', 'Pennsylvania'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='PA', max_length=40, verbose_name='state'),
        ),
        migrations.AddField(
            model_name='account',
            name='street_address',
            field=models.CharField(blank=True, help_text='example: 55 Linda Lane', max_length=100, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='account',
            name='zip_code',
            field=models.CharField(default=11111, max_length=5, verbose_name='zip code'),
            preserve_default=False,
        ),
    ]
