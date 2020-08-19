# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-01-06 07:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wildlifecompliance', '0362_auto_20200106_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='legalcase',
            name='associated_persons',
            field=models.ManyToManyField(related_name='legal_case_associated_persons', to=settings.AUTH_USER_MODEL),
        ),
    ]