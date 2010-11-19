from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^(index.html)?$','gus.views.index'),
    (r'^thanks.html$','gus.views.thanks'),
    (r'^thanks/$','gus.views.thanks'),
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^gus/', include('gus.gus_groups.urls')),
    (r'^admin/doc/?', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/?', include(admin.site.urls)),
)
