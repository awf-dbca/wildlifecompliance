# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-12-20 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0355_auto_20191220_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='remediationactiontaken',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]