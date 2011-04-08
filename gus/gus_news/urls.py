from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_news.views',
	(r'^_add/$', 'upload_form'),
)