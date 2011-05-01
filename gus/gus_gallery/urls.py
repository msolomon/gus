# GUS Gallery URLs
# Part of the GusPy Project
# Stephen Fischer
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
    (r'^group/([0-9]+)', 'gallery_group_list'),  # /gallery/group/<group id>/
    (r'^image/add/([0-9]+)', 'image_add'),       # /gallery/image/add/<gallery id>/
    (r'^image/delete/([0-9]+)', 'image_delete'), # /gallery/image/delete/<image id>/
    (r'^image/edit/([0-9]+)', 'image_edit'),     # /gallery/image/edit/<image id>/
    (r'^public/group/([0-9]+)', 'public_group'), # /gallery/public/group/<group id>/
    (r'^public', 'public_list'),                 # /gallery/public
    (r'^', 'index'),                             # /gallery/
)
