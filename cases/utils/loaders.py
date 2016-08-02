import csv
from cases.models import Case



def case_cop_loader(case_cop_file_path=None):
    if not case_cop_file_path:
        case_cop_file_path = '/home/matt/chicago-reporter/settlements/settlements/cops/migrations/casecops.csv'
    case_cop_file      = open(case_cop_file_path)
    case_cop_csv       = [x for x in csv.DictReader(case_cop_file)]
    for case_cop in case_cop_csv:
        cases = Case.objects.filter(case_no=case_cop['Case number'])
        try:
            assert len(list(cases)) == 1
        except Exception, e:
            print 'dupe case:', [x.id for x in cases]
            continue
        case = list(cases)[0]
        if case_cop['Cop ID']:
            cop        = Cop.objects.get(id=case_cop['Cop ID'])
            matched_by = 'script'
        else:
            cop        = None
            matched_by = None
        cc = CaseCop.objects.create(
                                    case               = case,
                                    case_no            = case_cop['Case number'],
                                    cop_first_name     = case_cop['First Name'],
                                    cop_middle_initial = case_cop['Middle Initial'],
                                    cop_last_name      = case_cop['Last Name'],
                                    badge_no           = case_cop['Badge Number'],
                                    officer_atty       = case_cop["Officer's Lead Attorney"],
                                    officer_atty_firm  = case_cop['Lead Attorney Law Firm'],
                                    entered_by         = case_cop['Entered By'],
                                    entered_when       = parse_str_date(case_cop['Timestamp']),
                                    fact_checked_by    = case_cop['Fact-checked by'],
                                    fact_checked_when  = parse_str_date(case_cop['Fact-checked date']),
                                    note               = case_cop['Note'],
                                    cop                = cop,
                                    matched_by         = matched_by,
                                   )
        print cc.__dict__
        #cc.save()


