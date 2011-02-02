# Gus Gallery Model Tests
# Part of the GUSPY effort
# Stephen Fischer
# January 2011
#
# TODO: Wait for whoever is dealing with gus_groups and gus_users to fix them? My tests fail because those can't init properly... unless I'm doing this wrong somewhere...
"""
This file contains the unit tests for the gus_gallery model
"""

from django.test import TestCase
from gus2.gus_gallery.models import *
from gus2.gus_groups.models import *
from gus2.gus_users.models import *

class gus_gallery_test(TestCase):
    def test_init(self):
        """
        Tests the gus_gallery object to see if it can be initiated
        """
        # Prepare a testing user/group
        the_user = gus_user(username="testuser", email="no@no.com", password="password")
        the_user.save()
        the_group = gus_group(groupname="Test Group")
        the_group.save()

        # If either the user or the group isn't set, then fail
        self.failIfEqual(the_user, None)
        self.failIfEqual(the_group, None)

        # Prepare a testing gallery
        the_gallery = gus_gallery(group=the_group, user=the_user, name="Test Gallery")
        the_gallery.save()

        # If the gallery doesn't exist, then fail
        self.failIfEqual(the_gallery, None)
        print("\ngus_gallery - init passed")

    def test_delete(self):
        """
        Tests the gus_gallery.delete() method
        """
        # Prepare a testing user/group
        the_user = gus_user(username="testuser", email="no@no.com", password="password")
        the_user.save()
        the_group = gus_group(groupname="Test Group")
        the_group.save()

        # If either the user or the group isn't set, then fail
        self.failIfEqual(the_user, None)
        self.failIfEqual(the_group, None)

        # Prepare a testing gallery
        the_gallery = gus_gallery(group=the_group, user=the_user, name="Test Delete Gallery")
        the_gallery.save()
        
        # If the gallery doesn't exist, then fail
        self.failIfEqual(the_gallery, None)

        # If the gallery existed, then we want to delete it and check again
        the_gallery.delete();

        self.failUnlessEqual(the_gallery, None)
        print("\ngus_gallery - delete passed")


    def test_add_image(self):
        """
        Tests the gus_gallery.add_image() method
        """
        # TODO: Implement the test


    def test_get_images(self):
        """
        Tests the gus_gallery.get_images() method
        """
        # TODO: Implement the test
