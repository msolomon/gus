from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_calendar.views',
    #(r'^', 'index')
    (r"^view/([A-Za-z]+)/(\d+)/$", "month"),
    (r"^", "index"),
)