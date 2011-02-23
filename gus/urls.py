import os
from django.conf import settings
from django.conf.urls.defaults import *
###############################################
#### Main URL Routing File          ###########
###############################################


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^gus/', include('gus.foo.urls')),
    (r'^gus_test/', include('gus.gusTestSuite.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	(r'^gallery/', include('gus.gus_gallery.urls')),
	(r'^emailer/', include('gus.gus_emailer.urls')),
	(r'^bill/', include('gus.gus_bill.urls')),
	(r'^gallery/', include('gus.gus_gallery.urls')),
	(r'^emailer/', include('gus.gus_emailer.urls')),
	(r'^forum/', include('gus.gus_forum.urls')),
	(r'^groups/', include('gus.gus_groups.urls')),
	(r'^calendar/', include('gus.gus_calendar.urls')),
	(r'^login/', 'gus.gus_users.views.login'),
	(r'^register/', 'gus.gus_users.views.register'),
	(r'^include/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, '..', 'media')})
	
    
)
