from django.shortcuts import render
from django.contrib.auth import authenticate, login
from cops.models import Cop, CaseCop, IPRACop
from cases.models import Case
from settlements.settings import LOGIN_REDIRECT_URL
from django.contrib.auth.views import login

from forms import FooForm, CopForm

from datetime import datetime, timedelta

# Create your views here.
def all_cops(request):
    if request.user.is_authenticated():
        return render(request,'all_cops.html',{'cops': Cop.objects.all()})


def all_casecops(request):
    if request.user.is_authenticated():
        case_cops = CaseCop.objects.all()
        unIDd_case_cops = sorted([x for x in case_cops if not x.cop], key = lambda x: (x.flag, x.case_no, x.cop_last_name))
        IDd_case_cops = sorted([x for x in case_cops if x.cop], key = lambda x: (x.flag, x.matched_by, x.case_no, x.cop_last_name),reverse=True )
        return render(request,'cases.html',{'unIDd_case_cops': unIDd_case_cops,'IDd_case_cops':IDd_case_cops})
    else:
        return login(request)


def all_ipracops(request):
    # TODO: abstract this
    if request.user.is_authenticated():
        ipra_cops = IPRACop.objects.all()
        unIDd_ipra_cops = sorted([x for x in ipra_cops if not x.cop], key = lambda x: (x.cr_no, x.cop_last_name))
        IDd_ipra_cops = sorted([x for x in ipra_cops if x.cop])
        return render(request,'ipra_cases.html',{'unIDd_ipra_cops': unIDd_ipra_cops,'IDd_ipra_cops':IDd_ipra_cops})
    else:
        return login(request)


def get_cop_label(cop):
    try:
        label = ''
        spacer = '     |     '
        label += cop.last_name + ', ' + cop.first_name + ' ' + cop.middle_init
        label += spacer    
        if cop.star_nos():
            stars = 'star(s): ' + ', '.join(cop.star_nos())
            label += stars
            label += spacer
        if cop.position_desc:
            label += cop.position_desc
            label += spacer
        if cop.cpd_unit_desc:
            label +=  cop.cpd_unit_desc
            label += spacer
        start_end = str(cop.appointed_date) + ' - ' + str(cop.resignation_date) 
        label += start_end
        label += spacer
        label += 'cop id: ' + str(cop.id)
        return label
    except Exception, e:
        import ipdb; ipdb.set_trace()


def casecop_detail(request, casecop_id):
    if request.user.is_authenticated():
        # get objects to set up page
        casecop = CaseCop.objects.get(id=casecop_id)
        flagged = casecop.flag
        cops = casecop.get_ordered_matches()
        if casecop.cop and casecop.cop not in cops:
            cops.append(casecop.cop)
        cs = [(cop.id, get_cop_label(cop)) for cop in cops]        
        cs.append((None,'None of the above'))
        #if casecop.cop:
        #    cops.insert(0,(casecop.cop.id, get_cop_label(casecop.cop)))
        selection = casecop.cop and casecop.cop.id or None
        note = casecop.note
        next_casecop_id = min(x.id for x in CaseCop.objects.all() if not x.cop and x.id != int(casecop_id) and not x.flag)
        
        # data updates, render page for POST
        if request.method == 'POST':
            form = CopForm(request.POST,choices=cs,selection=selection,flagged=flagged,note=note)
            if form.is_valid():
                if 'cop_choices' in form.data.keys():
                    cop_id = form.data['cop_choices']
                    if cop_id != 'None':
                        cop = Cop.objects.get(id=int(cop_id))
                    else:
                        cop = None
                    if cop != casecop.cop:
                        casecop.cop = cop
                        casecop.matched_by = request.user.username
                        casecop.matched_when = datetime.now() - timedelta(hours=5) #hack! 
                if 'flag' in form.data.keys():
                    casecop.flag = True
                else:
                    casecop.flag = False
                if 'note' in form.data.keys():
                    note = form.data['note']
                    casecop.note = note
                casecop.save()
                return render(request,'case_detail.html',{'casecop': casecop, 'form': form,'saved':True,'next_id':next_casecop_id})
            else:
                import ipdb; ipdb.set_trace()
        
        # render page for GET
        else:
            form = CopForm(choices=cs,initial={'cop_choices':selection},selection=selection,flagged=flagged,note=note)
            return render(request,'case_detail.html',{'casecop': casecop, 'form': form,'saved':False,'next_id':next_casecop_id})
   
    # login first
    else:
        return login(request)



def ipracop_detail(request, ipracop_id):
    if request.user.is_authenticated():
        # get objects to set up page
        ipracop = IPRACop.objects.get(id=ipracop_id)
        flagged = ipracop.flag
        cops = ipracop.get_ordered_matches()
        cs = [(cop.id, get_cop_label(cop)) for cop in cops]        
        cs.append((None,'None of the above'))
        #if casecop.cop:
        #    cops.insert(0,(casecop.cop.id, get_cop_label(casecop.cop)))
        selection = ipracop.cop and ipracop.cop.id or None
        note = ipracop.note
        next_ipracop_id = min(x.id for x in IPRACop.objects.all() if not x.cop and x.id != int(ipracop_id) and not x.flag)
        
        # data updates, render page for POST
        if request.method == 'POST':
            form = CopForm(request.POST,choices=cs,selection=selection,flagged=flagged,note=note)
            if form.is_valid():
                if 'cop_choices' in form.data.keys():
                    cop_id = form.data['cop_choices']
                    if cop_id != 'None':
                        cop = Cop.objects.get(id=int(cop_id))
                    else:
                        cop = None
                    ipracop.cop = cop
                    ipracop.matched_by = request.user.username
                    ipracop.matched_when = datetime.now() - timedelta(hours=5) #hack! 
                if 'flag' in form.data.keys():
                    ipracop.flag = True
                else:
                    ipracop.flag = False
                if 'note' in form.data.keys():
                    note = form.data['note']
                    ipracop.note = note
                ipracop.save()
                return render(request,'case_detail.html',{'casecop': ipracop, 'form': form,'saved':True,'next_id':next_ipracop_id})
            else:
                import ipdb; ipdb.set_trace()
        
        # render page for GET
        else:
            form = CopForm(choices=cs,initial={'cop_choices':selection},selection=selection,flagged=flagged,note=note)
            return render(request,'ipra_detail.html',{'ipracop': ipracop, 'form': form,'saved':False,'next_id':next_ipracop_id})
   
    # login first
    else:
        return login(request)
