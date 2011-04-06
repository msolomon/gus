from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_emailer.views',
	(r'user/([0-9]+)/','send'),
	(r'^$', 'check'),
	(r'^send', 'send'),
	(r'^check/message/(\d+)/?', 'check_message'),
	(r'^check_sent.*', 'check_sent'),
	(r'^check/(\d+)', 'check'),
	(r'^check', 'check'),
)
