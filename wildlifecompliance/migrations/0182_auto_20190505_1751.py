# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-05-05 09:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0181_auto_20190504_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callemail',
            name='location',
        ),
        migrations.AddField(
            model_name='location',
            name='call_email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='call_location', to='wildlifecompliance.CallEmail'),
        ),
    ]