'''
Created on Jan 15, 2011

@author: joran
'''
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('gus_roles.views',
    # Example:
    # (r'^gus/', include('gus.foo.urls')),
    (r'^add_user/([0-9]+)/', 'add_user_to_role'),
    (r'^', 'index'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
