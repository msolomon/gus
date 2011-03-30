'''
Created on Jan 15, 2011

@author: joran
'''
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('gus_groups.views',
    # Example:
    # (r'^gus/', include('gus.foo.urls')),
    (r'^/group/([0-9]+)/add_user/([0-9]+)/', 'add_user_to_role'),
    (r'^/group/([0-9]+)/Edit/(?P<role_id>\d+)/', 'editRole'),
    (r'^/group/([0-9]+)/New/(?P<group_id>\d+)/', 'createRole'),
    (r'^/group/([0-9]+)/EditPerms/(?P<role_id>\d+)/', 'editRolePerms'),
    (r'^/group/([0-9]+)/(?P<role_id>\d+)/RemoveUser/(?P<user_id>\d+)/', 'removeUserFromRole'),
    (r'^', 'index'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
