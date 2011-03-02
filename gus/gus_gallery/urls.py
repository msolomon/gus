# GUS Gallery URLs
# Part of the GUSPY effort
# Stephen Fischer
# February 2011
#
# Notes: All URL patterns below automatically have /gallery/ appended to their front

"""
This file matches the URLs for the GUS Gallery
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_gallery.views',
    (r'^([0-9])', 'single'),        # /gallery/5/
    (r'^add/', 'add'),              # /gallery/add/
    (r'^delete/([0-9])', 'delete'), # /gallery/delete/5/
    (r'^edit/([0-9])', 'edit'),     # /gallery/edit/5/
    (r'^', 'index'),                # /gallery/
)
