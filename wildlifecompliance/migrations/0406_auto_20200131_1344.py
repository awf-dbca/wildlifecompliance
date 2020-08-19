# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-01-31 05:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0405_briefofevidenceotherstatements'),
    ]

    operations = [
        migrations.AddField(
            model_name='briefofevidenceotherstatements',
            name='children',
            field=models.ManyToManyField(related_name='parents', to='wildlifecompliance.BriefOfEvidenceOtherStatements'),
        ),
        migrations.AddField(
            model_name='briefofevidenceotherstatements',
            name='ticked',
            field=models.BooleanField(default=False),
        ),
    ]