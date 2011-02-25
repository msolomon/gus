import time
import calendar
import datetime
##from django.contrib.auth.decorators import login_required
##from django.http import HttpResponseRedirect, HttpResponse
##from django.shortcuts import get_object_or_404, render_to_response

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from gus.gus_calendar.models import *


month_names = "January February March April May June July August September October November December"
month_names = month_names.split()

#print month_names
#print month_names[1]
#@login_regquired
#def index(request):
#    return render_to_response('calendar/index.html', {}, context_instance=RequestContext(request))

def index(request, year=None):
    if year: year = int(year)
    else: year = time.localtime()[0]
    
    current_year, current_month = time.localtime()[:2]
    list = []
    
    for m in [year, year + 1]: # calendar goes out 2 years
        month_list = []
        for n, month in enumerate(month_names):
            event = current = False
            events = Gus_event.objects.filter(start_date__year=m, start_date__month=n+1)
            if events:
                event = True # there is an event listed
            if m == current_year and  n + 1 == current_month:
                current = True # it is current month
            month_list.append(dict(n=n + 1, name=month, event=event, current=current))
        list.append((m, month_list))
        
        return render_to_response("calendar/index.html", {'years': list, 'year':year, 'month_names': month_names})
 
 
def month(request, month, year ):
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
    
    
    return render_to_response("calendar/month_view.html", {'year': year, 'month': month, 'month_name': month_name, 'month_days': list})
   
 
          

#def day(request, year, month, change=None):