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
    (r'^$','index'),
    (r'^([0-9]+)/CreateRole/', 'createRole'),
    (r'^EditPerms/([0-9]+)/', 'editRolePerms'),
    (r'^([0-9]+)/EditRole/([0-9]+)/', 'editRole'),
    (r'^([0-9]+)/Edit/', 'editGroupDesc'),
    (r'^Delete/([0-9]+)/', 'deleteGroup'),
    (r'^([0-9]+)/$', 'viewGroup'),
    (r'^([0-9]+)/Addsubgroup/', 'AddSubgroup'),
    (r'^Add/', 'addGroup'),
    #(r'^EditPerms/(?P<role_id>\d+)/', 'editRolePerms'),
    (r'^([0-9]+)/RemoveUser/(\d+)/', 'removeUserFromGroup'),
    (r'^ApproveGroup/','ApproveGroup'),
    #(r'^', 'index'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
