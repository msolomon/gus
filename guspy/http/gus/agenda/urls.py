from django.conf.urls.defaults import *
#from django.conf import settings

from models import *

info_dict = {
    'queryset'                  : Event.published.all(),
    'date_field'                : 'event_date',
    'template_object_name'      : 'event',
}

urlpatterns = patterns('gus.agenda.views.date_based',
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', info_dict,  name='agenda-detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',                  'archive',       info_dict,  name='agenda-archive-day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',                                   'archive',       info_dict,  name='agenda-archive-month'),
    url(r'^(?P<year>\d{4})/$',                                                      'archive',       info_dict,  name='agenda-archive-year'),
    url(r'^$',                                                                      'index',         info_dict,  name='agenda-index'),
)

ical_dict = {
    'queryset'                  : info_dict['queryset'],
    'date_field'                : info_dict['date_field'],
    'ical_filename'              : 'calendar.ics',
    'last_modified_field'       : 'mod_date',
    'location_field'            : 'location',
    'start_time_field'          : 'start_time',
    'end_time_field'            : 'end_time',
}

urlpatterns += patterns('gus.agenda.views.vobject_django',
    url(r'^calendar.ics$',                                                          'icalendar',     ical_dict,  name='agenda-icalendar'),
)
