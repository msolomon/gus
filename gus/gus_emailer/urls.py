from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_emailer.views',
	(r'user/(\d+)/','send'),
	(r'^$', 'check'),
	(r'^send/(.*)', 'send'),
	(r'^group/(\d+)', 'send_group'),
	(r'^check/message/(\d+)/?', 'check_message'),
	(r'^check_sent.*', 'check_sent'),
	(r'^check/(\d+)', 'check'),
	(r'^check', 'check'),
)
