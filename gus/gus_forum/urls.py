"""
This file matches the URLs for the GUS Gallery
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_forum.views',
	(r'^', 'index'),
)
