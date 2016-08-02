"""
the whole point here is
to make sure we don't confuse
duplicate-named cops
"""
import csv
from cops.models import Cop, CaseCop
from settlements.settings import BASE_DIR




def casecops_with_dupes():
    """
    it's better to look up cops
    with same name as casecops, then
    verify casecop
    """
    ### CONFIG START ###
    outfile_dir  = BASE_DIR + '/reports/output/'
    outfile_path = outfile_dir + 'ambiguous.csv'
    ### CONFIG END   ###
    outfile      = open(outfile_path,'w')
    headers      = [
                    'casecop_id',
                    'case_id',
                    'case_no',
                    'casecop_cop_name',
                    'casecop_cop_badge',
                    'cop_id',
                    'cop_first_name',
                    'cop_middle_init',
                    'cop_last_name',
                    'cop_badge_nos',
                    'cop_position_desc',
                    'cop_unit_desc',
                    'other_cop_id',
                    'other_cop_first_name',
                    'other_cop_middle_init',
                    'other_cop_last_name',
                    'other_cop_badge_nos',
                    'other_cop_position_desc',
                    'other_cop_unit_desc',
                    'matched_by',
                    'matched_when',
                    'flagged',
                   ]

    outcsv       = csv.DictWriter(outfile, headers)
    outcsv.writeheader()

    casecops = [x for x in CaseCop.objects.all() if x.cop]
    
    for casecop in casecops:
        case              = casecop.case
        cop               = casecop.cop
        raw_dopplegangers = list(Cop.objects.filter(
                                                first_name = cop.first_name,
                                                last_name  = cop.last_name,
                                               ))
        dopplegangers = []
        for doppleganger in raw_dopplegangers:
            # let's cut the chase and call it if there's a badge number confirmation
            if casecop.badge_no and casecop.badge_no in cop.star_nos():
                continue

            # filter out the actual casecop
            if doppleganger != cop:

                # can't use incident date if there isn't one ... throw them all in
                if not case.incident_date:
                    dopplegangers.append(doppleganger)
                    continue

                # started after the incident ... continue
                if doppleganger.appointed_date and doppleganger.appointed_date > case.incident_date:
                    continue

                # retired before the incident ... continue
                if doppleganger.resignation_date and doppleganger.resignation_date < case.incident_date:
                    continue

                # middle initial exists and doesn't match ... continue
                if casecop.cop_middle_initial and doppleganger.middle_init and casecop.cop_middle_initial != doppleganger.middle_init:
                    continue

                # well, it could be a dupe ...
                dopplegangers.append(doppleganger)

        for doppleganger in dopplegangers:
            row = {
                    'casecop_id'              : casecop.id,
                    'case_id'                 : case.id,
                    'case_no'                 : case.case_no,
                    'casecop_cop_name'        : casecop.cop_first_name + ' ' + (casecop.cop_middle_initial + ' ' if casecop.cop_middle_initial else '') + casecop.cop_last_name,
                    'casecop_cop_badge'       : casecop.badge_no,
                    'cop_id'                  : cop.id,
                    'cop_first_name'          : cop.first_name,
                    'cop_middle_init'         : cop.middle_init,
                    'cop_last_name'           : cop.last_name,
                    'cop_badge_nos'           : '|'.join(cop.star_nos()),
                    'cop_position_desc'       : cop.position_desc,
                    'cop_unit_desc'           : cop.cpd_unit_desc, 
                    'other_cop_id'            : doppleganger.id ,
                    'other_cop_first_name'    : doppleganger.first_name,
                    'other_cop_middle_init'   : doppleganger.middle_init,
                    'other_cop_last_name'     : doppleganger.last_name,
                    'other_cop_badge_nos'     : '|'.join(doppleganger.star_nos()),  
                    'other_cop_position_desc' : doppleganger.position_desc,
                    'other_cop_unit_desc'     : doppleganger.cpd_unit_desc,
                    'matched_by'              : casecop.matched_by,
                    'matched_when'            : casecop.matched_when,
                    'flagged'                 : casecop.flag,
                  }

            outcsv.writerow(row)

    outfile.close()



def dupe_cops():
    """
    identify cops 
    with duplicate names so we 
    can double-check them
    """
    ### CONFIG START ###
    output_path  = BASE_DIR + '/reports/output/'
    outfile_path = output_path + 'dupes.csv'
    ### CONFIG END   ###
    outfile = open(outfile_path,'w')
    headers = [
               'cop_id', 
               'first_name',
               'last_name',
               'appointed_date',
               'resignation_date',
               'star(s)',
               'case id(s)',
               'case no(s)',
              ]
    outcsv  = csv.DictWriter(outfile,headers)
    outcsv.writeheader()

    slug_cops = {}

    for cop in Cop.objects.all():
        slug = cop.first_name + cop.last_name
        if slug not in slug_cops:
            slug_cops[slug] = []
        slug_cops[slug].append(cop)

    dupe_slugs = [slug for slug in slug_cops.keys() if len(slug_cops[slug]) > 1]

    for slug in dupe_slugs:
        for cop in slug_cops[slug]:
            for cc in cop.casecop_set.all():
                row =  {
                        'cop_id'           : cop.id, 
                        'first_name'       : cop.first_name,
                        'last_name'        : cop.last_name,
                        'appointed_date'   : cop.appointed_date,
                        'resignation_date' : cop.resignation_date,
                        'star(s)'          : '|'.join([cs.star for cs in cop.copstar_set.all()]),
                        'case id(s)'       : '|'.join([str(cc.id) for cc in cop.casecop_set.all()]),
                        'case no(s)'       : '|'.join([cc.case_no for cc in cop.casecop_set.all()]),
                       }
                outcsv.writerow(row)
        #import ipdb; ipdb.set_trace()
    outfile.close()
