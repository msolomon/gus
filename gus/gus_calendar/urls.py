from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_calendar.views',
    #(r'^', 'index')
    (r"^(\d+)/([A-Za-z]+)/_edit(\d+)/(\d+)/$", "day_edit"),
    (r"^(\d+)/([A-Za-z]+)/_add(\d+)/$", "day_add"),
    (r"^(\d+)/([A-Za-z]+)/(\d+)/(\d+)/$", "day_view"),
    (r"^(\d+)/([A-Za-z]+)/(\d+)/view_events/$", "view_all"),
    (r"^group(\d+)/(\d+)/([A-Za-z]+)/$", "month"), #for group
    (r"^(\d+)/([A-Za-z]+)/$", "month"), # for user
    (r"^", "month"),
    
    ## add group_id later
)