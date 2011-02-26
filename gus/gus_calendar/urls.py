from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_calendar.views',
    #(r'^', 'index')
    (r"^day/(\d+)/(\d+)/(\d+)/$", "day"),
    (r"^view/([A-Za-z]+)/(\d+)/$", "month"),
    (r"^", "index"),
    
    
)