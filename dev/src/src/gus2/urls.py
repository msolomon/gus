from django.conf.urls.defaults import *
###############################################
#### Main URL Routing File          ###########
###############################################


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^gus2/', include('gus2.foo.urls')),
    (r'^gus_test/',include('gus2.gusTestSuite.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
