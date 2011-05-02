import time
import calendar
from datetime import date, datetime
from django import forms
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from gus.gus_calendar.models import *
from gus.gus_groups.utils import *
from gus.gus_roles.models import *

month_names = "January February March April May June July August September October November December"
month_names = month_names.split()
years = []

#print month_names
#print month_names[1]
#def index(request):
#    return render_to_response('calendar/index.html', {}, context_instance=RequestContext(request))

def month(request, year=None, month=None):
     if not request.user.is_authenticated():
         return HttpResponseRedirect('/login/')
     #groups = getGroupsWithUser(request.user)

     if year: year = int(year)
     else: year = time.localtime()[0]

     current_year, current_month = time.localtime()[:2]
     if month:
         month_name = month
         for i in range(0, len(month_names)):
             if month == month_names[i]:
                 month = (i+1)
         month_list = []
         years = [] ## have to reset or get duplicates!!!
     else:
        month = time.localtime()[1]
        years = [] ## have to reset or get duplicates!!!
            
     for m in [year]: # calendar goes out 2 years
        month_list = []
     for n, month_name in enumerate(month_names):
        current = False
        #events = Gus_event.objects.filter(start_date__year=m, start_date__month=n+1)
        #if events:
        #    event = True # there is an event listed
        if m == current_year and  n + 1 == current_month:
            current = True # it is current month
        month_list.append(dict(n=n + 1, name=month_name, current=current))
     years.append((m, month_list))
     month_name = month_names[month-1]

## for months        
     user_groups = getGroupsWithUser(request.user)
     num_total_events = 0
     cal = calendar.Calendar()
     month_days = cal.itermonthdays(year, month)
     nyear, nmonth, nday = time.localtime()[:3]
     list = [[]]
     #total_day_events = []
     week = 0
     total_events = []
     count = 0
     for day in month_days:
        #for group in groups:
        events = current = False
        if day:
            ##group_ids = [user_group.id for user_group in user_groups]
            events = Gus_event.objects.filter(start_date__year=year, 
                                              start_date__month=month, 
                                              start_date__day=day,
                                              Group__in=user_groups)
                
            num_total_events += len(events) 
            if day == nday and year == nyear and month == nmonth: 
                current = True
            total_events.append(events)

        list[week].append((day, total_events, current, num_total_events))
        num_total_events = 0
        if len(list[week]) == 7:
             list.append([])
             week = week + 1
        total_events = []
     #year = time.localtime()[0]
     
    
     return render_to_response("calendar/month_view.html",
                               {'year': year,
                                'yearminus': (year-1),
                                'yearplus': (year+1), 
                                'years': years, 
                                'month_name': month_name, 
                                'month_days': list,
                                'month_list': month_list,
                                'total_events':total_events}, 
                                context_instance=RequestContext(request))
   

def view_all(request, year, month, day):
    total_day_events = []
    usr = request.user
    groups = getGroupsWithUser(usr)
    
    auth_groups = [user_group for user_group in groups if usr.has_group_perm(user_group, 'Can add gus_event')]

    
    month_name = month
    month = month_names.index(month) + 1
    for group in groups:
        events = Gus_event.objects.filter(start_date__year=year, start_date__month=month, start_date__day=day, Group=group.id)
        total_day_events.append(events)
    return render_to_response("calendar/view_events.html",
                              {'year':year,
                               'month_name': month_name,
                               'day':day,
                               'total_day_events':total_day_events,
                               'auth_groups': auth_groups},
                               context_instance=RequestContext(request))
          
          
@login_required           
def day_view(request, year, month, day, event_id):
    usr = request.user
    groups = getGroupsWithUser(usr)

 
    month_name = month
    month = month_names.index(month) + 1
    
    
    event = Gus_event.objects.get(pk=event_id)
    event_creator = event.creator
    event_description = event.description
    event_name = event.event_name
    event_group = event.Group
    if not usr.has_group_perm(event_group, 'Can add gus_event'):
        auth_event_group = 0
    else: auth_event_group = 1
    return render_to_response("calendar/day_view.html",
                              {'year':year,
                               'month_name':month_name, 
                               'day':day,
                               'creator':event.creator,
                               'description': event.description,
                               'name': event.event_name,
                               'start_date': event.start_date,
                               'start_time': event.start_time,
                               'event_id': event_id,
                               'event_group':event_group,
                               'auth_event_group': auth_event_group}, 
                               context_instance=RequestContext(request))
    
        

@login_required
def day_add(request, year, month, day): #, group_id):
    ## user permission authenticity ##
    auth_groups = []
    usr = request.user  
    groups = getGroupsWithUser(usr)
    for group in groups:

        if usr.has_group_perm(group, 'Can add gus_event'):
            auth_groups.append(group)
    if len(auth_groups) == 0:
        return HttpResponseRedirect('calendar/month_view.html')
## -------------------------------------------------------##            
        
    month_name = month
    month = month_names.index(month) + 1

    if request.method == "POST":
        form = Event_form(request.POST)
        from django.forms.extras.widgets import SelectDateWidget ##group permission to add event
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = usr
            event.start_date = date(int(year), int(month), int(day))
            
            event.save()
            event_group = event.Group
            response = request.META['HTTP_REFERER'].rstrip('/')
            print response
            splice = response.rfind('/')
            return HttpResponseRedirect(response[:splice] + '/')
            
    else:
        ## check if user is allowed to add events and display those groups
        auth_groups = []
        usr = request.user      
        groups = getGroupsWithUser(usr)
        for group in groups:
            if usr.has_group_perm(group, 'Can add gus_event'):
                auth_groups.append(group)
        if len(auth_groups) == 0:
            return HttpResponseRedirect('calendar/month_view.html')
        ##------------------------------------------##
        form = Event_form()
        ## display groups user has permissions for ##
        gids = [g.id for g in groups if usr.has_group_perm(g, 'Can add gus_event')]
        form.fields['Group'].queryset = gus_group.objects.filter(pk__in=gids)
        
        
    return render_to_response("calendar/add_event.html", 
                              {'event_form': form,
                               'event_group': Group, 
                               'month_name':month_name, 
                               'year':year, 
                               'day':day}, 
                               context_instance=RequestContext(request)) 


@login_required
def day_edit(request, year, month, day, event_id): #, group_id):
    usr = request.user
    
 
    edit = Gus_event.objects.get(pk=event_id)
    
    month_name = month
    month = month_names.index(month) + 1

    if request.method == "POST":
        form = Event_form_edit(request.POST, instance = edit) 
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = usr
            event.start_date = date(int(year), int(month), int(day))
            event.save()
            if event.Delete == True: ## if delete is checked, delete that event!
                event.delete()
            response = request.META['HTTP_REFERER']
            splice = response.rfind('_')
            return HttpResponseRedirect(response[:splice])
            
    else:
        edit = Gus_event.objects.get(pk=event_id)
        form = Event_form_edit(instance=edit)
        
    return render_to_response("calendar/day_edit_view.html", 
                              {'event_form': form, 
                               'month_name':month_name, 
                               'year':year,
                               'day': day, 
                               'event_id':event_id,
                               'group': False}, # No, this is NOT a group calendar 
                               context_instance=RequestContext(request))
    
    
def group_month(request, group_id, year=None, month=None):
     try:
        group = gus_group.objects.get(pk = group_id) ## if there is a group
        print group
     except:
        return HttpResponse('Group Not Found.')
        

     if year: year = int(year)
     else: year = time.localtime()[0]
     
     current_year, current_month = time.localtime()[:2]
     if month:
         month_name = month
         for i in range(0, len(month_names)):
             if month == month_names[i]:
                 month = (i+1)
         month_list = []
         years = [] ## have to reset or get duplicates!!!
     else:
        month = time.localtime()[1]
        years = [] ## have to reset or get duplicates!!!
            
     for m in [year]: # calendar goes out 2 years
        month_list = []
     for n, month_name in enumerate(month_names):
        current = False
        #events = Gus_event.objects.filter(start_date__year=m, start_date__month=n+1)
        #if events:
        #    event = True # there is an event listed
        if m == current_year and  n + 1 == current_month:
            current = True # it is current month
        month_list.append(dict(n=n + 1, name=month_name, current=current))
     years.append((m, month_list))
     month_name = month_names[month-1]

## for months
     num_total_events = 0
     cal = calendar.Calendar()
     month_days = cal.itermonthdays(year, month)
     nyear, nmonth, nday = time.localtime()[:3]
     list = [[]]
     #total_day_events = []
     week = 0
     total_events = []
     count = 0
     for day in month_days:
        #for group in groups:
        events = current = False
        if day:
            events = Gus_event.objects.filter(start_date__year=year, 
                                              start_date__month=month, 
                                              start_date__day=day,
                                              Group=group)
            if day == nday and year == nyear and month == nmonth: 
                    current = True
            total_events.append(events)
            
        list[week].append((day, total_events, current, num_total_events))
        num_total_events = 0
        if len(list[week]) == 7:
             list.append([])
             week = week + 1
        total_events = []
#     year = time.localtime()[0]
    
    
     return render_to_response("calendar/month_view.html",
                               {'group': True, ## yes, this is a group calendar
                                'group_name':group.group_name,
                                'group_id':group_id,
                                'year': year,
                                'yearminus': (year-1),
                                'yearplus': (year+1), 
                                'years': years, 
                                'month_name': month_name, 
                                'month_days': list,
                                'month_list': month_list,
                                'total_events':total_events}, 
                                context_instance=RequestContext(request))    
     
     
@login_required
def group_day_add(request, group_id, year, month, day): #, group_id):
    ## user permission authenticity ##
    auth_groups = []
    usr = request.user
    try:
        group = gus_group.objects.get(pk = group_id) ## if there is a group
    except:
        return HttpResponse('Group Not Found.')  
    if usr.has_group_perm(group, 'Can add gus_event'):
            auth_groups.append(group)
    else:
        return HttpResponseRedirect('calendar/month_view.html')
## -------------------------------------------------------##            
        
    month_name = month
    month = month_names.index(month) + 1

    if request.method == "POST":
        form = Event_form(request.POST)
        from django.forms.extras.widgets import SelectDateWidget ##group permission to add event
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = usr
            event.start_date = date(int(year), int(month), int(day))
            
            event.save()
            event_group = event.Group
            response = request.META['HTTP_REFERER'].rstrip('/')
            #print response
            splice = response.rfind('/')
            return HttpResponseRedirect(response[:splice] + '/')
            
    else:
        ## check if user is allowed to add events and display those groups
        auth_groups = []
        usr = request.user
        try:
            group = gus_group.objects.get(pk = group_id) ## if there is a group
        except:
            return HttpResponse('Group Not Found.')  
        if usr.has_group_perm(group, 'Can add gus_event'):
                auth_groups.append(group)
        else:
            return HttpResponseRedirect('calendar/month_view.html')
        ##------------------------------------------##
        form = Event_form()
        ## display groups user has permissions for ##
        if usr.has_group_perm(group, 'Can add gus_event'):
            form.fields['Group'].queryset = gus_group.objects.filter(pk=group_id)
        
        
    return render_to_response("calendar/add_event.html", 
                              {'event_form': form,
                               'event_group': group, 
                               'month_name':month_name, 
                               'year':year, 
                               'day':day}, 
                               context_instance=RequestContext(request)) 
