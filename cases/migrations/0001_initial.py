# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-12 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_no', models.CharField(max_length=30)),
                ('date_filed', models.DateTimeField(null=True)),
                ('date_closed', models.DateTimeField(null=True)),
                ('judge', models.CharField(max_length=30)),
                ('plaintiff_atty', models.CharField(max_length=30)),
                ('plaintiff_firm', models.CharField(max_length=30)),
                ('city_atty', models.CharField(max_length=30)),
                ('city_firm', models.CharField(max_length=30)),
                ('magistrate', models.CharField(max_length=30)),
                ('incident_date', models.DateField(null=True)),
                ('location', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('state', models.CharField(max_length=100, null=True)),
                ('lat', models.FloatField(null=True)),
                ('lon', models.FloatField(null=True)),
                ('census_place', models.CharField(max_length=6, null=True)),
                ('census_msa', models.CharField(max_length=6, null=True)),
                ('census_met_div', models.CharField(max_length=6, null=True)),
                ('census_mcd', models.CharField(max_length=6, null=True)),
                ('census_micro', models.CharField(max_length=6, null=True)),
                ('census_cbsa', models.CharField(max_length=6, null=True)),
                ('census_block', models.CharField(max_length=6, null=True)),
                ('census_block_g', models.CharField(max_length=6, null=True)),
                ('census_tract', models.CharField(max_length=6, null=True)),
                ('census_county', models.CharField(max_length=6, null=True)),
                ('census_state', models.CharField(max_length=6, null=True)),
                ('naaccr_cert', models.CharField(max_length=6, null=True)),
                ('m_number', models.CharField(max_length=6, null=True)),
                ('m_predirection', models.CharField(max_length=6, null=True)),
                ('m_name', models.CharField(max_length=30, null=True)),
                ('m_suffix', models.CharField(max_length=6, null=True)),
                ('m_city', models.CharField(max_length=20, null=True)),
                ('m_state', models.CharField(max_length=20, null=True)),
                ('narrative', models.CharField(max_length=1000, null=True)),
                ('causes', models.TextField()),
                ('tags', models.TextField()),
                ('reporter', models.CharField(max_length=20)),
                ('fact_checker', models.CharField(max_length=20)),
                ('differences', models.CharField(max_length=1000)),
                ('notes', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='IPRACase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cr_no', models.IntegerField(unique=True)),
                ('incident_date', models.DateTimeField()),
                ('complaint_date', models.DateField()),
                ('category_code', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
    ]
