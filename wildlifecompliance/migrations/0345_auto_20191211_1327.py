# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-12-11 05:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wildlifecompliance', '0344_auto_20191211_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentartifact',
            name='custodian',
        ),
        migrations.RemoveField(
            model_name='physicalartifact',
            name='custodian',
        ),
        migrations.AddField(
            model_name='artifact',
            name='custodian',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artifact_custodian', to=settings.AUTH_USER_MODEL),
        ),
    ]
