from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_emailer.views',
	(r'user/([0-9]+)/','send'),
	(r'^$', 'send'),
	(r'^user/check/', 'check')
)
