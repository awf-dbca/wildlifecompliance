# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-09-09 01:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0295_auto_20190905_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='inspection_team',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
