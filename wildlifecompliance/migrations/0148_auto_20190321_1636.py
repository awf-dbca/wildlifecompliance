# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-03-21 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0147_merge_20190314_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='callemail',
            name='assigned_to',
            field=models.CharField(default='brendan', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='callemail',
            name='caller',
            field=models.CharField(default='Jawaid', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='callemail',
            name='lodged_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='callemail',
            name='number',
            field=models.CharField(default='default', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classification',
            name='name',
            field=models.CharField(choices=[('complaint', 'Complaint'), ('enquiry', 'Enquiry'), ('incident', 'Incident')], default='complaint', max_length=30),
        ),
    ]
