###############################################
#### Main URL Routing File          ###########
###############################################
import os
from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$','gus.gus_users.views.welcome'),
    (r'^gus_test/', include('gus.gusTestSuite.urls')),
	(r'^gallery/', include('gus.gus_gallery.urls')),
	(r'^emailer/', include('gus.gus_emailer.urls')),
	(r'^bill/', include('gus.gus_bill.urls')),
	(r'^gallery/', include('gus.gus_gallery.urls')),
	(r'^email/', include('gus.gus_emailer.urls')),
	(r'^forum/', include('gus.gus_forum.urls')),
	(r'^groups/', include('gus.gus_groups.urls')),
	(r'^roles/', include('gus.gus_Roles.urls')),
	(r'^calendar/', include('gus.gus_calendar.urls')),
	(r'^login/', 'gus.gus_users.views.loginView'),
        (r'^logout/', 'gus.gus_users.views.logoutView'),
	(r'^register/', 'gus.gusTestSuite.views.addUser'),
	(r'^include/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, '..', 'media')}),
        (r'^users/',include('gus.gus_users.urls')),
        (r'^news/',include('gus.gus_news.urls')),
)
