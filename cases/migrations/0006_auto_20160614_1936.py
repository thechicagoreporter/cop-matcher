# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-14 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
            ('cases', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='causes',
        ),
        migrations.AddField(
            model_name='case',
            name='federal_causes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='interaction_type',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='misconduct_type',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='officers',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='outcome',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='primary_cause',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='proactive_reactive',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='state_causes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='submitted_by',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='victims',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='weapons_used',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
