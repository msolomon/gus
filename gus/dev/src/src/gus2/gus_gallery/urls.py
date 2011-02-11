from django.conf.urls.defaults import *
###############################################
#### Main URL Routing File          ###########
###############################################


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('gus2.gus_gallery.views',
    (r'^/', 'index'),
)
