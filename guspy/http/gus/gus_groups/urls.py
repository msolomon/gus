from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('gus.gus_groups.views',
    # Example:
    # (r'^gus/', include('gus.foo.urls')),
    (r'^index.html?$','index'),
    (r'^$','index'),
    (r'^create_group/$','create_group'),
    (r'^test_manager.html?$','super_manager'),
    (r'^user/test_manager.html?$','super_user_manager'),
    (r'^user/(\d+)/view/?$','user_detail_view'),
    (r'^group/test_manager.html?$','super_group_manager'),
)
