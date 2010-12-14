from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('gus.gus_groups.views',
    # Example:
    # (r'^gus/', include('gus.foo.urls')),
    (r'^installdummies/([a-zA-Z0-9])/',dummy_setup)
    (r'^index.html?$','index'),
    (r'^$','index'),
    (r'import^$','import_users'),
    (r'^create_group/$','create_group'),
#    (r'^test_manager.html?$','super_manager'),
    (r'^user/test_manager.html?$','super_user_manager'),
    (r'^user/(\d+)/view/?$','user_detail_view'),
    (r'^group/(\d+)/view/?$','view_group'),
    (r'^group/(\d+)/administer/?$','groupadmin'),
    (r'^([a-z_A-Z0-9]+)/([a-zA-Z]+)','group_module'),#this needs to be last in list or it will over match
#    (r'^group/test_manager.html?$','super_group_manager'),
)
