from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_emailer.views',
	(r'user/([0-9]+)/','email_user'),
	(r'^$', 'index')
)
