import time
##from django.contrib.auth.decorators import login_required
##from django.http import HttpResponseRedirect, HttpResponse
##from django.shortcuts import get_object_or_404, render_to_response
from gus.gus_calendar.models import *


month_names = "January February March April May June July August September October November December"
month_names = month_names.split()

#@login_regquired

def main(request, year=None):
    if year: year = int(year)
    else: year = time.localtime()[0]
    
    current_year, current_month = time.localtime()[:2]
    list = []
    
    for m in [year, year + 1]: # calendar goes out 2 years
        month_list = []
        for n, month in enumerate(month_names):
            if Event:
                item = True # there is an event listed
            if m == current_year and  n + 1 == current_month:
                current = True
            month_list.append(dict(n=n + 1, name=month, event_name=item, current=current))
        list.append((m, month_list))
        
        
 
        ##return render_to_response("blahblah/main.html", dict(years=list, user=request.user, year=year))
  
def month(request, year, month, change=None):
    year, month = int(year), int(month)
    ##finish this                    
