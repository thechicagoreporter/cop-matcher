from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Case(models.Model):
    """
    source:
    initial data entry
    cases.xlsx
    """
    case_no            = models.CharField(max_length=30)
    date_filed         = models.DateTimeField(null=True) 
    date_closed        = models.DateTimeField(null=True)
    judge              = models.CharField(max_length=30)
    plaintiff_atty     = models.CharField(max_length=30)
    plaintiff_firm     = models.CharField(max_length=30)
    city_atty          = models.CharField(max_length=30)
    city_firm          = models.CharField(max_length=30)
    magistrate         = models.CharField(max_length=30)
    incident_date      = models.DateField(null=True)
    
    location           = models.CharField(max_length=50,null=True)
    address            = models.CharField(max_length=100,null=True)
    city               = models.CharField(max_length=100,null=True)
    state              = models.CharField(max_length=100,null=True)
    lat                = models.FloatField(null=True) 
    lon                = models.FloatField(null=True) 
    census_place       = models.CharField(max_length=6,null=True)
    census_msa         = models.CharField(max_length=6,null=True)
    census_met_div     = models.CharField(max_length=6,null=True)
    census_mcd         = models.CharField(max_length=6,null=True)
    census_micro       = models.CharField(max_length=6,null=True)
    census_cbsa        = models.CharField(max_length=6,null=True)
    census_block       = models.CharField(max_length=6,null=True)
    census_block_g     = models.CharField(max_length=6,null=True)
    census_tract       = models.CharField(max_length=6,null=True)
    census_county      = models.CharField(max_length=6,null=True)
    census_state       = models.CharField(max_length=6,null=True)
    naaccr_cert        = models.CharField(max_length=6,null=True)
    m_number           = models.CharField(max_length=6,null=True)
    m_predirection     = models.CharField(max_length=6,null=True)
    m_name             = models.CharField(max_length=30,null=True)
    m_suffix           = models.CharField(max_length=6,null=True)
    m_city             = models.CharField(max_length=20,null=True)
    m_state            = models.CharField(max_length=20,null=True)
    
    narrative          = models.CharField(max_length=1000,null=True)
    primary_cause      = models.TextField() # hack
    federal_causes     = models.TextField() # hack
    state_causes       = models.TextField() # hack
    interaction_type   = models.TextField() # hack
    proactive_reactive = models.TextField() # hack
    officers           = models.TextField()
    victims            = models.TextField()
    misconduct_type    = models.TextField()
    weapons_used       = models.TextField()
    outcome            = models.TextField()
    submitted_by       = models.TextField()
    tags               = models.TextField() # hack
    reporter           = models.CharField(max_length=20)
    fact_checker       = models.CharField(max_length=20)
    differences        = models.CharField(max_length=1000)
    notes              = models.CharField(max_length=1000)


class IPRACase(models.Model):
    cr_no          = models.IntegerField(unique=True)
    incident_date  = models.DateTimeField()
    complaint_date = models.DateField()
    category_code  = models.CharField(max_length=10)
    description    = models.CharField(max_length=100)


class Payment(models.Model):
    case_no              = models.CharField(max_length=20)
    case                 = models.ForeignKey(Case)
    payee                = models.CharField(max_length=100)
    payment              = models.IntegerField()
    fees_costs           = models.IntegerField()
    primary_cause        = models.CharField(max_length=50)
    primary_cause_edited = models.CharField(max_length=50)
    department           = models.CharField(max_length=50)
    disposition          = models.CharField(max_length=50)
    disposition_true     = models.CharField(max_length=50)
    date_paid            = models.DateField()
    misconduct           = models.BooleanField()
