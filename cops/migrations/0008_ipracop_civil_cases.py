# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-16 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cops', '0007_ipracop_tiebreakers'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipracop',
            name='civil_cases',
            field=models.ManyToManyField(to='cops.CaseCop'),
        ),
    ]