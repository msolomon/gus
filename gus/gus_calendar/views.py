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


def month(request, year=None, month=None):
    
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
        month = time.localtime()[2]
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
    
    
     return render_to_response("calendar/month_view.html",
                               {'year': year, 
                                'years': years, 
                                'month_name': month_name, 
                                'month_days': list,
                                'month_list': month_list, 
                                'events':events}, 
                                context_instance=RequestContext(request))
   

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
        
    return render_to_response("calendar/day_view.html", 
                              {'event_form': form, 
                               'month_name':month_name, 
                               'year':year, 'day':day}, 
                               context_instance=RequestContext(request)) #add_csrf(request, events=form, year=year, month=month, day=day))
    



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
        
    return render_to_response("calendar/day_edit_view.html", 
                              {'event_form': form, 
                               'month_name':month_name, 
                               'year':year, 
                               'day':day}, 
                               context_instance=RequestContext(request)) #add_csrf(request, events=form, year=year, month=month, day=day))
    
    
    