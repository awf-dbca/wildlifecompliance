# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-03 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooring', '0064_auto_20180920_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='mooringsitebooking',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=8, null=True),
        ),
    ]