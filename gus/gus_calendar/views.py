import time
import calendar
from datetime import date, datetime
from django import forms
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.models import modelformset_factory

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from gus.gus_calendar.models import *


month_names = "January February March April May June July August September October November December"
month_names = month_names.split()
years = []

#print month_names
#print month_names[1]
#@login_regquired
#def index(request):
#    return render_to_response('calendar/index.html', {}, context_instance=RequestContext(request))

def index(request, year=None):
    if year: year = int(year)
    else: year = time.localtime()[0]
    
    current_year, current_month = time.localtime()[:2]
    #list = []
    
    for m in [year, year + 2]: # calendar goes out 2 years
        month_list = []
        for n, month in enumerate(month_names):
            event = current = False
            events = Gus_event.objects.filter(start_date__year=m, start_date__month=n+1)
            if events:
                event = True # there is an event listed
            if m == current_year and  n + 1 == current_month:
                current = True # it is current month
            month_list.append(dict(n=n + 1, name=month, event=event, current=current))
        years.append((m, month_list))
        
        current_month_name = month_names[current_month-1]
        
            
        

        ## this is mostly just so the current month is displayed first
        cal = calendar.Calendar()
        month_days = cal.itermonthdays(year, current_month)
        nyear, nmonth, nday = time.localtime()[:3]
        dlist = [[]]
        week = 0
        
        for day in month_days:
            events = current = False
            if day:
                events = Gus_event.objects.filter(start_date__year=year, start_date__month=current_month, start_date__day=day)
                if day == nday and year == nyear and month == nmonth: 
                    current = True
            
            dlist[week].append((day, events, current))
            if len(dlist[week]) == 7:
                dlist.append([])
                week = week + 1
        
        return render_to_response("calendar/month_view.html", {'years': years, 'year':year, 'month_names': month_names, "current_month_name": current_month_name, "year": current_year, "month_days": dlist})
 
 
def month(request, year, month):
    #year, month = int(year), int(month)
    year = int(year)
    month_name = month
    #print len(month_names)
    for i in range(0, len(month_names)):
        if month == month_names[i]:
            month = (i+1)
    
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    list = [[]]
    week = 0
    
    for day in month_days:
        events = current = False
        if day:
            events = Gus_event.objects.filter(start_date__year=year, start_date__month=month, start_date__day=day)
            if day == nday and year == nyear and month == nmonth: 
                current = True
        
        list[week].append((day, events, current))
        if len(list[week]) == 7:
            list.append([])
            week = week + 1
    
    
    return render_to_response("calendar/month_view.html", {'year': year, 'month': month, 'month_name': month_name, 'month_days': list, 'years': years, 'events':events})
   

#          
#class Event_form(forms.Form):
#    event_name = forms.CharField(max_length = 60)
#    event_description = forms.CharField(widget=forms.Textarea)
#    
        


def day(request, year, month, day):
    month_name = month
    month = month_names.index(month) + 1

    if request.method == "POST":

        form = Event_form(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            #for event in events:
            #event.creator = request.user
            event.start_date = date(int(year), int(month), int(day))
            event.save()

#            return HttpResponseRedirect("calendar/month_view.html")
            response = request.META['HTTP_REFERER'].rstrip('/')
            splice = response.rfind('/')
            return HttpResponseRedirect(response[:splice] + '/')
            
    else:
        form = Event_form()
        
    return render_to_response("calendar/day_view.html", {'event_form': form, 'month_name':month_name, 'year':year, 'day':day}, context_instance=RequestContext(request)) #add_csrf(request, events=form, year=year, month=month, day=day))
    



def day_edit(request, year, month, day):
    month_name = month
    month = month_names.index(month) + 1

    if request.method == "POST":

        #edit = Gus_event.objects.get(creator=request.user)
        edit = Gus_event.objects.get(pk=1)
        form = Event_form(request.POST, instance=edit) 
        print "editing"
        if form.is_valid():
            event = form.save()
                #event = form.save(commit=False)
            #for event in events:
            #event.creator = request.user
                #event.start_date = date(int(year), int(month), int(day))
            #if form.fields['delete'] != False:
             #   event.delete_event()

#            return HttpResponseRedirect("calendar/month_view.html")
            response = request.META['HTTP_REFERER'].rstrip('/')
            splice = response.rfind('/')
            return HttpResponseRedirect(response[:splice] + '/')
            
    else:
        form = Event_form()
        
    return render_to_response("calendar/day_edit_view.html", {'event_form': form, 'month_name':month_name, 'year':year, 'day':day}, context_instance=RequestContext(request)) #add_csrf(request, events=form, year=year, month=month, day=day))
    
    
    