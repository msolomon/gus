# GUS Gallery URLs
# Part of the GUSPY effort
# Stephen Fischer
# February 2011

"""
This file matches the URLs for the GUS Gallery
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_bill.views',
    (r'^', 'index'))
