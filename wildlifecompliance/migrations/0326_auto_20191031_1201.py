# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-10-31 04:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0325_sanctionoutcomeduedateconfiguration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sanctionoutcome',
            old_name='penalty_amount',
            new_name='penalty_amount_1st',
        ),
    ]