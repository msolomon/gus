'''
Created on Jan 15, 2011

@author: joran
'''
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('gus2.gusTestSuite.views',
    # Example:
    # (r'^gus2/', include('gus2.foo.urls')),
    (r'^$', 'index'),
    
    (r'^Group/Add/$', 'addGroup'),
    (r'^Group/Edit/(?P<group_id>\d+)/$', 'editGroup'),
    (r'^Group/Delete/(?P<group_id>\d+)/', 'deleteGroup'),
    
    (r'^User/Add', 'addUser'),
    (r'^User/Edit/(?P<user_id>\d+)/', 'editUser'),
    (r'^User/Delete/(?P<user_id>\d+)/', 'deleteUser'),
    
    (r'^Role/Edit/(?P<role_id>\d+)/', 'editRole'),
    (r'^Role/(?P<role_id>\d+)/RemoveUser/(?P<user_id>\d+)/', 'removeUserFromRole'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
