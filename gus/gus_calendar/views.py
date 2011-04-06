import time
import calendar
from datetime import date, datetime
from django import forms
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm


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
#@login_regquired
#def index(request):
#    return render_to_response('calendar/index.html', {}, context_instance=RequestContext(request))

def month(request, year=None, month=None):
     if not request.user.is_authenticated():
         return HttpResponseRedirect('/login/')
     groups = getGroupsWithUser(request.user)
    
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
        event = current = False
        events = Gus_event.objects.filter(start_date__year=m, start_date__month=n+1)
        if events:
            event = True # there is an event listed
        if m == current_year and  n + 1 == current_month:
            current = True # it is current month
        month_list.append(dict(n=n + 1, name=month_name, event=event, current=current))
     years.append((m, month_list))
     month_name = month_names[month-1]

## for months
     cal = calendar.Calendar()
     month_days = cal.itermonthdays(year, month)
     nyear, nmonth, nday = time.localtime()[:3]
     list = [[]]
     #total_day_events = []
     week = 0
    
     for day in month_days:
        #for group in groups:
        events = current = False
        if day:
            events = Gus_event.objects.filter(start_date__year=year, start_date__month=month, start_date__day=day)
            #total_day_events.append(events) 
            if day == nday and year == nyear and month == nmonth: 
                current = True
        
        list[week].append((day, events, current))
        if len(list[week]) == 7:
             list.append([])
             week = week + 1
     year = time.localtime()[0]
    
    
     return render_to_response("calendar/month_view.html",
                               {'year': year, 
                                'years': years, 
                                'month_name': month_name, 
                                'month_days': list,
                                'month_list': month_list}, 
#                                'group_id': group_id}, 
                                context_instance=RequestContext(request))
   

def view_all(request, year, month, day):
    month_name = month
    month = month_names.index(month) + 1
    
    events = Gus_event.objects.filter(start_date__year=year, start_date__month=month, start_date__day=day)
    return render_to_response("calendar/view_events.html",
                              {'year':year,
                               'month_name': month_name,
                               'day':day,
                               'events':events},
                               context_instance=RequestContext(request))
          
          
                    
def day_view(request, year, month, day, event_id):
    not_auth = 0
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    usr = request.user
    groups = getGroupsWithUser(usr)
    for group in groups:
        if not usr.has_group_perm(group, 'Can add event'):
            not_auth = 1 # if user not authorized, display list of events only
    
 
    month_name = month
    month = month_names.index(month) + 1
    
    
    event = Gus_event.objects.get(pk=event_id)
    event_creator = event.creator
    event_description = event.description
    event_name = event.event_name
    
    return render_to_response("calendar/day_view.html",
                              {'year':year,
                               'month_name':month_name, 
                               'day':day,
                               'creator':event.creator,
                               'description': event.description,
                               'name': event.event_name,
                               'start_date': event.start_date,
                               'event_id': event_id,
                               'not_auth': not_auth}, 
                               context_instance=RequestContext(request))
    
        


def day_add(request, year, month, day): #, group_id):
    auth_groups = []
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    usr = request.user
    groups = getGroupsWithUser(usr)
    print groups
    for group in groups:
        print gus_role.objects.with_user(usr)
        if not usr.has_group_perm(group, 'Can add event'):
            return HttpResponseRedirect('calendar/month_view.html')
        else:
            auth_groups.append(group)
            
        
    month_name = month
    month = month_names.index(month) + 1

    if request.method == "POST":

        form = Event_form(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = usr
            event.start_date = date(int(year), int(month), int(day))
            event.groups = auth_groups
            event.save()

            response = request.META['HTTP_REFERER'].rstrip('/')
            print response
            splice = response.rfind('/')
            return HttpResponseRedirect(response[:splice] + '/')
            
    else:
        form = Event_form()
        
    return render_to_response("calendar/add_event.html", 
                              {'event_form': form, 
                               'month_name':month_name, 
                               'year':year, 
                               'day':day},
                               #'group_id': group_id}, 
                               context_instance=RequestContext(request)) 



def day_edit(request, year, month, day, event_id): #, group_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
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
                               'event_id':event_id},
#                               'group_id': group_id}, 
                               context_instance=RequestContext(request)) #add_csrf(request, events=form, year=year, month=month, day=day))
    
    
    
