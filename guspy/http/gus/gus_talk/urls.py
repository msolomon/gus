from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('gus.gus_talk.views',
    # Example:
    (r'^$','main'),
    (r'^forum/(\d+)/$','forum'),
    (r'^thread/(\d+)/$','thread'),
    # Uncomment the admin/doc line below to enable admin documentation:
)
