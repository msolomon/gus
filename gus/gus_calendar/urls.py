from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_calendar.views',
    #(r'^', 'index')
    (r"^(\d+)/([A-Za-z]+)/(\d+)/$", "day"),
    (r"^(\d+)/([A-Za-z]+)/$", "month"),
    (r"^", "index"),
    
    
)