# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-20 23:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation_finance', '0032_auto_20170720_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorConflict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=150)),
                ('origin', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('conflict_description', models.CharField(max_length=300, verbose_name='Conflict description')),
                ('conflict_resolution', models.CharField(blank=True, max_length=300, null=True, verbose_name='Conflict resolution')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='conflict',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='conflict_description',
        ),
        migrations.AddField(
            model_name='invoice',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/operations_invoice/', verbose_name='File'),
        ),
        migrations.AddField(
            model_name='vendorconflict',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conflict', to='operation_finance.Invoice'),
        ),
    ]
