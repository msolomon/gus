# GUS Gallery URLs
# Part of the GUSPY effort
# Stephen Fischer
# February 2011

"""
This file matches the URLs for the GUS Gallery
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('gus2.gus_gallery.views',
    (r'^', 'index'),
    (r'^group/([a-zA-z0-9])/', 'group'),
    (r'^([0-9])', 'single'),
)
