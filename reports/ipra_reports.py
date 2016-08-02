import csv
from cops.models import Cop, CaseCop, IPRACop
from cases.models import Case, IPRACase
from settlements.settings import BASE_DIR
from datetime import date, timedelta

### CONFIG START ###
output_path     = BASE_DIR + '/reports/output/'
### CONFIG END   ###


def run_unmatched_ipracop_report():
    ### CONFIG START ###
    output_filepath = output_path + 'unmatched_ipracops.csv'
    date_delta      = 0
    ### CONFIG END   ###
    
    outfile = open(output_filepath,'w')
    headers = [
               'cr no',
               'incident date',
               'description',
               'ipracop id',
               'ipracop first name',
               'ipracop last name',
               'ipracop badge no',
               'matching civil case nos',
               'matching civil case ids',
               'officers named'
              ]
    outcsv   = csv.DictWriter(outfile,headers)
    outcsv.writeheader()

    unmatched_ipra_cops = [ x for x in IPRACop.objects.all() if not x.cop]

    for icop in unmatched_ipra_cops:
        ipra_case            = icop.case
        inc_date             = ipra_case.incident_date.date() 
        matching_civil_cases = list(Case.objects.filter(incident_date=inc_date))
        matching_case_cops   = []
        for case in matching_civil_cases:
            for casecop in case.casecop_set.all():
                cop = casecop.cop
                if cop:
                    matching_case_cops.append(cop.first_name + ' ' + cop.last_name)
                else:
                    print 'no cop for casecop.id', casecop.id
        row = {
                'cr no'                   : ipra_case.cr_no,
                'incident date'           : inc_date,
                'description'                : ipra_case.description,
                'ipracop id'              : ipra_case.id,
                'ipracop first name'      : icop.cop_first_name,
                'ipracop last name'       : icop.cop_last_name,
                'ipracop badge no'        : icop.badge_no,
                'matching civil case nos' : '|'.join([x.case_no for x in matching_civil_cases]),
                'matching civil case ids' : '|'.join([str(x.id) for x in matching_civil_cases]),
                'officers named'          : '|'.join(cop for cop in matching_case_cops),
              }
        outcsv.writerow(row)
    outfile.close()

def run_report():
    ### CONFIG START ###
    output_filepath = output_path + 'civil_and_ipra.csv'
    date_delta      = 2
    ### CONFIG END   ###

    outfile = open(output_filepath,'w')
    headers = [
               'Civil Case No.',
               'Officer First Name', 
               'Officer Last Name',
               'CivilCase ID',
               'Cop ID',
               'CaseCop ID',
               'IPRACase IDs',
               'IPRA CR Nos',
               'IPRACop IDs',
              ]
    outcsv = csv.DictWriter(outfile,headers)
    outcsv.writeheader()

    civil_casecops = [x for x in CaseCop.objects.all() if x.cop]

    for cc in civil_casecops:
        case                    = cc.case
        cop                     = cc.cop
        ipra_cases              = [ ic.case for ic in cop.ipracop_set.all() if dates_are_close(case,ic.case,date_delta) ] 
        ipra_cops               = []
        for ipra_case in ipra_cases:
            for ipra_cop in ipra_case.ipracop_set.all():
                if ipra_cop.cop == cop:
                    ipra_cops.append(ipra_cop)
        row = {
                'Civil Case No.'     : case.case_no,
                'Officer First Name' : cop.first_name, 
                'Officer Last Name'  : cop.last_name,
                'CivilCase ID'       : case.id,
                'Cop ID'             : cop.id,
                'CaseCop ID'         : cc.id,
                'IPRACase IDs'       : '|'.join(set([str(x.id) for x in ipra_cases])),
                'IPRA CR Nos'        : '|'.join(set([str(x.cr_no) for x in ipra_cases])),
                'IPRACop IDs'        : '|'.join(set([str(icop.id) for icop in ipra_cops])) 
              }
        outcsv.writerow(row)

    outfile.close()


def dates_are_close(civil_case, ipra_case,date_delta):
    """
    return boolean
    if IPRA case incident
    was within few days
    """
    civil_incident_date = civil_case.incident_date
    ipra_incident_date  = ipra_case.incident_date.date() if ipra_case else None
    if civil_incident_date and ipra_incident_date:
        delta               = timedelta(days=date_delta)
        early_boundary      = civil_incident_date - delta
        later_boundary      = civil_incident_date + delta
        return (ipra_incident_date >= early_boundary) and (ipra_incident_date <= later_boundary) 

