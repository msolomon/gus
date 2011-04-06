'''
Created on Jan 15, 2011

@author: joran
'''
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('gusTestSuite.views',
    # Example:
    # (r'^gus/', include('gus.foo.urls')),
    (r'^$','index2'),
    (r'^([0-9]+)/CreateRole/', 'createRole'),
    (r'^([0-9]+)/Edit/', 'editGroup'),
    (r'^Add/', 'addGroup'),
    #(r'^EditPerms/(?P<role_id>\d+)/', 'editRolePerms'),
    (r'^([0-9]+)/RemoveUser/(\d+)/', 'removeUserFromGroup'),
    #(r'^', 'index'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
