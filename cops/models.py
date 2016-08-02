from __future__ import unicode_literals
from django.db import models
from cases.models import Case, IPRACase
import re
from datetime import date, datetime

# Create your models here.
class Cop(models.Model):
    """
    source:
    city badge list or
    invisible institute list
    """
    last_name        = models.CharField(max_length=20)
    first_name       = models.CharField(max_length=20)
    middle_init      = models.CharField(max_length=5)
    sex              = models.CharField(max_length=5)
    race             = models.CharField(max_length=30)
    dob_year         = models.IntegerField(null=True)
    current_age      = models.IntegerField(null=True)
    status           = models.BooleanField()
    appointed_date   = models.DateField(null=True)
    position_code    = models.CharField(max_length=5)
    position_desc    = models.CharField(max_length=40)
    cpd_unit         = models.CharField(max_length=5)
    cpd_unit_desc    = models.CharField(max_length=55)
    resignation_date = models.DateField(null=True)
    # slug = last_name + first_name + start_date
    slug             = models.CharField(max_length=100) # this should be unique 
    notes            = models.TextField(null=True)
    def star_nos(self):
        # TODO: test
        return [x.star for x in CopStar.objects.filter(cop=self)]


class CopStar(models.Model):
    cop  = models.ForeignKey(Cop)
    star = models.CharField(max_length=10) 


class ListedCop(models.Model):
    """
    gets inherited
    by casecop, ipracop for
    sharing match logic
    """
    # basic cop stuff
    cop                = models.ForeignKey(Cop, blank=True, null=True)
    cop_first_name     = models.CharField(max_length=20)
    cop_middle_initial = models.CharField(max_length=5)
    cop_last_name      = models.CharField(max_length=20)
    badge_no           = models.CharField(max_length=10)
    note               = models.CharField(max_length=1000)
    flag               = models.NullBooleanField(default=False)
    matched_by         = models.CharField(max_length=10)
    matched_when       = models.DateTimeField(null=True)


    ### MATCHING START ###
    # how many letters to start a partial
    partial_match_len = 5


    def strip_lower(self, name):
        """
        lower-case, remove
        special characters to do
        name comparisons
        """
        return re.sub("[^a-zA-Z]+", "",name).lower()


    def name_match(self,case_name,sworn_name,chars=None):
        """
        check if given names
        match after controlling for
        case, spaces and length
        """
        return self.strip_lower(case_name)[:chars] == self.strip_lower(sworn_name)[:chars]


    def get_matches(self):
        matches = {}
        cops = Cop.objects.all()
        matches['partial_last_name'] = [cop for cop in cops if self.cop_last_name and self.name_match(self.cop_last_name, cop.last_name, self.partial_match_len)]
        matches['full_last_name']    = [cop for cop in matches['partial_last_name'] if self.name_match(self.cop_last_name, cop.last_name)]
        matches['partial_first_name'] = [cop for cop in cops if self.cop_first_name and self.name_match(self.cop_first_name, cop.first_name, self.partial_match_len)]
        matches['full_first_name']    = [cop for cop in matches['partial_first_name'] if self.name_match(self.cop_first_name, cop.first_name)]
        matches['badge_no'] = self.cops_matching_badge_no()
        return matches


    def qualify_matches(self):
        matches = self.get_matches()
        
        # partial last name match, plus either first name and/or badge (unless they're not available)
        matches['potential'] = [match for match in matches['partial_last_name'] if match in matches['partial_first_name'] or match in matches['badge_no']]
        # and let's do some date filtering here even tho we call this again later in the casecop_detail view ...
        matches['potential'] = self.filter_by_date(matches['potential'])
        # full last name match, plus either first name and/or badge 
        matches['probable']  = [match for match in matches['potential'] if match in matches['full_last_name'] or match in matches['badge_no']]
        if len(matches['probable']) > 1:
            # if not scalar result, see if badge_matches breaks the tie
            probable_with_badge_match = [match for match in matches['probable'] if match in matches['badge_no']]
            if probable_with_badge_match:
                matches['probable'] = probable_with_badge_match
        # TODO: sanity checks: dates, badge numbers can exclude

        return matches


    def cops_matching_badge_no(self):
        return [x.cop for x in CopStar.objects.all() if x.star and x.star.strip() == self.badge_no.strip()]


    def first_2_letters_last_name_match(self, last_name):
        if self.cop_last_name and last_name:
            return self.cop_last_name[0:2].lower() == last_name[0:2].lower()

    @property
    def cops_matching_names(self):
        name_matches = []
        for cop in Cop.objects.all():
            if cop.last_name and cop.last_name[:4].lower() == self.cop_last_name[:4].lower():
                if not self.cop_first_name:
                    pass # first name isn't necessary to match
                else:
                    if cop.first_name and cop.first_name[0].lower() != self.cop_first_name[0].lower():
                        continue # not a match if first name mismatched
                name_matches.append(cop)
        return name_matches


    def get_ordered_matches(self):
        try:
            cops = []
            # ordering matters because we want the best matches first
            for matchtype in ['probable','full_last_name','partial_last_name','badge_no']:
                for cop in self.qualify_matches()[matchtype]:
                    if cop not in cops:
                        cops.append(cop) 
            filtered_cops = self.filter_by_date(cops)
            return filtered_cops
        except Exception, e:
            import ipdb; ipdb.set_trace()


    def filter_by_date(self,cops):
        """ 
        candidates shouldn't
        have worked outside of the date
        listed in complaint
        """
        inc_date = self.case.incident_date
        try:
            if type(inc_date) != date:
                inc_date = inc_date.date()
        except Exception, e:
            import ipdb; ipdb.set_trace()
        # the weirdest shit happens when you try to mutate a list (or copy) during iteration!!!
        filtered_cops = [x for x in cops]
        if inc_date:
            # we can only filter by date if there's an incident date
            for cop in cops:
                if cop.resignation_date and cop.resignation_date < inc_date:
                    # cop resigned before incident ... remove this cop
                    filtered_cops.remove(cop)
                    continue
                if cop.appointed_date and cop.appointed_date > inc_date:
                    # cop was hired after incident ... remove this cop
                    filtered_cops.remove(cop)
        return filtered_cops


    @property
    def get_matches_old(self):
        return [x for x in (set(self.cops_matching_names + self.cops_matching_badge_no)) if self.first_2_letters_last_name_match(x.last_name)]

    class Meta:
        abstract = True


class CaseCop(ListedCop):
    """
    source:
    initial data entry
    Officers - sample.csv
    """
    # case stuff
    case               = models.ForeignKey(Case)
    case_no            = models.CharField(max_length=20)
    slug               = models.CharField(max_length=50)

    # cop stuff
    officer_atty       = models.CharField(max_length=100)
    officer_atty_firm  = models.CharField(max_length=100)
    
    # reporter/audit stuff
    entered_by        = models.CharField(max_length=20)
    entered_when      = models.DateField(null=True)
    fact_checked_by   = models.CharField(max_length=20)
    fact_checked_when = models.DateField(null=True)


class IPRACop(ListedCop):
    """
    source:
    CPD FOIA
    ipra_officers.csv
    """
    case            = models.ForeignKey(IPRACase)
    cr_no           = models.IntegerField()
    finding         = models.CharField(max_length=10)
    discipline_code = models.CharField(max_length=5)
    discipline      = models.CharField(max_length=50)

    # i.e., which IPRA cases relate to a given Civil case ...
    # ... currently unused because we can across ORM to get this
    civil_cases     = models.ManyToManyField(CaseCop)
