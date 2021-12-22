# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-11-23 05:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0553_callemail_brief_nature_of_call'),
    ]

    operations = [
        migrations.AddField(
            model_name='callemail',
            name='entangled',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('no', 'No'), ('fishing_line', 'Fishing Line'), ('rope', 'Rope'), ('string', 'String'), ('wire', 'Wire'), ('other', 'Other')], max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='callemail',
            name='call_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='call_type', to='wildlifecompliance.CallType'),
            preserve_default=False,
        ),
    ]
