from cops.models import Cop, CaseCop, CopStar
from cases.models import Case, Payment
from settlements.settings import BASE_DIR
import unicodecsv as csv

### CONFIG START ###
output_dir                = BASE_DIR + '/reports/output/'
cop_report_file_name      = output_dir + 'cops.csv'
casecop_report_file_name  = output_dir + 'casecops.csv'
case_report_file_name     = output_dir + 'case.csv'
copstar_report_file_name  = output_dir + 'copstars.csv'
payment_report_file_name  = output_dir + 'payments.csv'
### CONFIG END ###

# create files
cop_report_file     = open(cop_report_file_name,'w')
casecop_report_file = open(casecop_report_file_name,'w')
case_report_file    = open(case_report_file_name,'w')
copstar_report_file = open(copstar_report_file_name,'w')
payment_report_file = open(payment_report_file_name,'w')

# build headers
# cop_report_fields     = [field.name for field in Cop._meta.fields]
cop_report_fields = [
                     'id',
                     'last_name',
                     'first_name',
                     'middle_init',
                     'sex',
                     'race',
                     'dob_year',
                     'current_age',
                     'status',
                     'appointed_date',
                     'position_code',
                     'position_desc',
                     'cpd_unit',
                     'cpd_unit_desc',
                     'resignation_date',
                     'slug',
                     'notes'
                    ]

#casecop_report_fields = [field.name for field in CaseCop._meta.fields]
#casecop_report_fields.remove('cop') 
#casecop_report_fields.remove('case') 
#casecop_report_fields += ['case_id', 'cop_id']
casecop_report_fields = [
                         'id',
                         'case_no',
                         'slug',
                         'cop_first_name',
                         'cop_middle_initial',
                         'cop_last_name',
                         'badge_no',
                         'officer_atty',
                         'officer_atty_firm',
                         'entered_by',
                         'entered_when',
                         'fact_checked_by',
                         'fact_checked_when',
                         'matched_by',
                         'matched_when',
                         'note',
                         'flag',
                         'case_id',
                         'cop_id'
                        ]


#case_report_fields    = [field.name for field in Case._meta.fields]
case_report_fields = [
                        'id',
                        'CaseNumber',
                        'DateFiled',
                        'DateClosed',
                        'Judge',
                        'PlaintiffsLeadAttorney',
                        'PlaintiffsAttorneyLawFirm',
                        'CitysLeadAttorney',
                        'CitysAttorneyLawFirm',
                        'MagistrateJudge',
                        'DateofIncident',
                        'LocationListed',
                        'StreetAddress',
                        'City',
                        'State',
                        'EnteredBy',
                        'Fact-checkedby',
                        'Differences',
                        'Latitude',
                        'Longitude',
                        'CensusPlaceFips',
                        'CensusMsaFips',
                        'CensusMetDivFips',
                        'CensusMcdFips',
                        'CensusCbsaMicro',
                        'CensusCbsaFips',
                        'CensusBlock',
                        'CensusBlockGroup',
                        'CensusTract',
                        'CensusCountyFips',
                        'CensusStateFips',
                        'naaccrCertCode',
                        'MNumber',
                        'MPreDirectional',
                        'MName',
                        'MSuffix',
                        'MCity',
                        'MState',
                        'Narrative',
                        'primary_cause',
                        'federal_causes',
                        'state_causes',
                        'interaction_type',
                        'officers',
                        'victims',
                        'misconduct_type',
                        'weapons_used',
                        'outcome',
                        'tags'
                     ]

copstar_report_fields = ['cop_id','star']

payment_report_fields = [
                         'case_num',
                         'payee',
                         'payment',
                         'fees_costs',
                         'primary_case',
                         'disposition',
                         'date_paid'
                        ]

#payment_report_fields = [field.name for field in Payment._meta.fields]
#payment_report_fields.remove('case')
#payment_report_fields.append('case_id')

# make csv
cop_report_csv     = csv.DictWriter(cop_report_file,cop_report_fields)
casecop_report_csv = csv.DictWriter(casecop_report_file,casecop_report_fields)
case_report_csv    = csv.DictWriter(case_report_file,case_report_fields)
copstar_report_csv = csv.DictWriter(copstar_report_file,copstar_report_fields)
payment_report_csv = csv.DictWriter(payment_report_file,payment_report_fields)

# write headers
cop_report_csv.writeheader()
casecop_report_csv.writeheader()
case_report_csv.writeheader()
copstar_report_csv.writeheader()


# roll through
for cop in Cop.objects.all():
    #cop_dict = dict((field,getattr(cop,field)) for field in cop_report_csv.fieldnames)
    cop_dict = {
                 'id': cop.id,
                 'last_name': cop.last_name,
                 'first_name': cop.first_name,
                 'middle_init': cop.middle_init,
                 'sex': cop.sex,
                 'race': cop.race,
                 'dob_year': cop.dob_year,
                 'current_age': cop.current_age,
                 'status': cop.status,
                 'appointed_date': cop.appointed_date,
                 'position_code': cop.position_code,
                 'position_desc': cop.position_desc,
                 'cpd_unit': cop.cpd_unit,
                 'cpd_unit_desc': cop.cpd_unit_desc,
                 'resignation_date': cop.resignation_date,
                 'slug': cop.slug,
                 'notes': cop.notes
               }

    cop_report_csv.writerow(cop_dict)



filtered_casecops = [x for x in CaseCop.objects.all()]

for casecop in filtered_casecops:
    #casecop_dict = dict((field,getattr(casecop,field)) for field in casecop_report_csv.fieldnames)
    #casecop_dict['case_id'] = casecop.case.id
    #casecop_dict['cop_id'] = casecop.cop.id if casecop.cop else None
    casecop_dict = {
                     'id': casecop.id,
                     'case_no': casecop.case_no,
                     'slug': casecop.slug,
                     'cop_first_name': casecop.cop_first_name,
                     'cop_middle_initial': casecop.cop_middle_initial,
                     'cop_last_name': casecop.cop_last_name,
                     'badge_no': casecop.badge_no,
                     'officer_atty': casecop.officer_atty,
                     'officer_atty_firm': casecop.officer_atty_firm,
                     'entered_by': casecop.entered_by,
                     'entered_when': casecop.entered_when,
                     'fact_checked_by': casecop.fact_checked_by,
                     'fact_checked_when': casecop.fact_checked_when,
                     'matched_by': casecop.matched_by,
                     'matched_when': casecop.matched_when,
                     'note': casecop.note,
                     'flag': casecop.flag,
                     'case_id': casecop.case.id,
                     'cop_id': casecop.cop.id if casecop.cop else None
                   }
    try:
        casecop_report_csv.writerow(casecop_dict)
    except Exception, e:
        import ipdb; ipdb.set_trace()


for case in Case.objects.all():
    try:
        #case_dict = dict((field,getattr(case,field)) for field in case_report_csv.fieldnames)
        case_dict = {
                    'id': case.id,
                    'CaseNumber': case.case_no,
                    'DateFiled': case.date_filed,
                    'DateClosed': case.date_closed,
                    'Judge': case.judge,
                    'PlaintiffsLeadAttorney': case.plaintiff_atty,
                    'PlaintiffsAttorneyLawFirm': case.plaintiff_firm,
                    'CitysLeadAttorney': case.city_atty,
                    'CitysAttorneyLawFirm': case.city_firm,
                    'MagistrateJudge': case.magistrate,
                    'DateofIncident': case.incident_date,
                    'LocationListed': case.location,
                    'StreetAddress': case.address,
                    'City': case.city,
                    'State': case.state,
                    'EnteredBy': case.submitted_by,
                    'Fact-checkedby': case.fact_checker,
                    'Differences': case.differences,
                    'Latitude': case.lat,
                    'Longitude': case.lon,
                    'CensusPlaceFips': case.census_place,
                    'CensusMsaFips': case.census_msa,
                    'CensusMetDivFips': case.census_met_div,
                    'CensusMcdFips': case.census_mcd,
                    'CensusCbsaMicro': case.census_micro,
                    'CensusCbsaFips': case.census_cbsa,
                    'CensusBlock': case.census_block,
                    'CensusBlockGroup': case.census_block_g,
                    'CensusTract': case.census_tract,
                    'CensusCountyFips': case.census_tract,
                    'CensusStateFips': case.census_state,
                    'naaccrCertCode': case.census_state,
                    'MNumber': case.m_number,
                    'MPreDirectional': case.m_predirection,
                    'MName': case.m_name,
                    'MSuffix': case.m_suffix,
                    'MCity': case.m_city,
                    'MState': case.m_state,
                    'Narrative': case.narrative,
                    'primary_cause': case.primary_cause,
                    'federal_causes': case.federal_causes,
                    'state_causes': case.state_causes,
                    'interaction_type': case.interaction_type,
                    'officers': case.officers,
                    'victims': case.victims,
                    'misconduct_type': case.misconduct_type,
                    'weapons_used': case.weapons_used,
                    'outcome': case.outcome,
                    'tags': case.tags
             }

        case_report_csv.writerow(case_dict)
    except Exception, e:
        import ipdb; ipdb.set_trace()


for copstar in CopStar.objects.all():
    copstar_dict = {'cop_id': copstar.cop.id, 'star': copstar.star}
    copstar_report_csv.writerow(copstar_dict)


for payment in Payment.objects.all():
    #payment_dict = dict((field,getattr(payment,field)) for field in payment_report_csv.fieldnames)
    #payment_dict['case_id'] = payment.case.id
    payment_dict = {
                    'case_num': payment.case_no,
                    'payee': payment.payee,
                    'payment': payment.payment,
                    'fees_costs': payment.fees_costs,
                    'primary_case': payment.primary_cause_edited,
                    'disposition': payment.disposition_true,
                    'date_paid': payment.date_paid
                   }
    payment_report_csv.writerow(payment_dict)


# close files
cop_report_file.close()
casecop_report_file.close()
case_report_file.close()
copstar_report_file.close()
payment_report_file.close()
