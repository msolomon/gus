from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_news.views',
    (r'^', 'upload_form'),
)