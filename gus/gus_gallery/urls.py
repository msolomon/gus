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

urlpatterns = patterns(
    'gus.gus_gallery.views',
    (r'^([0-9]+)', 'gallery_view'),              # /gallery/<gallery id>/
    (r'^add/([0-9]+)', 'gallery_add'),           # /gallery/add/<group id>/
    (r'^delete/([0-9]+)', 'gallery_delete'),     # /gallery/delete/<gallery id>/
    (r'^edit/([0-9]+)', 'gallery_edit'),         # /gallery/edit/<gallery id>/
    (r'^image/add/([0-9]+)', 'image_add'),       # /gallery/image/add/<gallery id>/
    (r'^image/delete/([0-9]+)', 'image_delete'), # /gallery/image/delete/<image id>/
    (r'^image/edit/([0-9]+)', 'image_edit'),     # /gallery/image/edit/<image id>/
    (r'^', 'index'),                            # /gallery/
)
