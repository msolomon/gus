# Gus Gallery Model Tests
# Part of the GUSPY effort
# Stephen Fischer
# February 2011

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
        the_user = gus_user.objects.create_user(username="testuser", email="no@no.com", password="password")
        the_user.save()
        the_group = gus_group.objects.create_group(groupname="Test Group")
        the_group.save()

        # If either the user or the group isn't set, then fail the test
        self.failIfEqual(the_user, None, "Could not initialize test user.")
        self.failIfEqual(the_group, None, "Could not initialize test group.")

        ## TEST 1 - Create a valid gallery belonging to a group
        the_gallery = gus_gallery.objects.create(group=the_group, user=the_user, name="Test Gallery")
        #the_gallery.save()
        self.failIfEqual(the_gallery, None, "Could not initialize test gallery.")

        ## TEST 2 - Try to create incomplete galleries, fail if they work
        try:
            the_gallery = gus_gallery(group=None, user=the_user, name="Test Gallery 2")
            self.failIfNotEqual(the_gallery, None, "Created invalid gallery without a group.")
        except:
            # Do nothing
            the_gallery = None
        try:
            the_gallery = gus_gallery(group=the_group, user=None, name="Test Gallery 3")
            self.failIfNotEqual(the_gallery, None, "Created invalid gallery without a user.")
        except:
            # Do nothing
            the_gallery = None
        try:
            the_gallery = gus_gallery(group=None, user=None, name="Test Gallery 4")
            self.failIfNotEqual(the_gallery, None, "Created invalid gallery without a group or user.")
        except:
            # Do nothing
            the_gallery = None


    def test_delete(self):
        """
        Tests the gus_gallery.delete() method
        """
        # Prepare a testing user/group
        the_user = gus_user.objects.create_user(username="testuser", email="no@no.com", password="password")
        the_user.save()
        the_group = gus_group.objects.create_group(groupname="Test Group")
        the_group.save()

        # If either the user or the group isn't set, then fail
        self.failIfEqual(the_user, None, "Could not initialize test user.")
        self.failIfEqual(the_group, None, "Could not initialize test group.")

        ## TEST 1 - Create a valid gallery, so we can test deleting it. If we can't create a group, fail this test
        the_gallery = gus_gallery(group=the_group, user=the_user, name="Test Delete Gallery")
        the_gallery.save()
        self.failIfEqual(the_gallery, None, "Could not initialize test gallery.")

        the_gallery.delete()
        self.failIfEqual(the_gallery, None, "Test gallery not successfully deleted")


    def test_add_image(self):
        """
        Tests the gus_gallery.add_image() method
        """
        # Create testing user, group, and gallery objects
        the_user = gus_user.objects.create_user(username="testuser", email="no@no.com", password="password")
        the_user.save()
        the_group = gus_group.objects.create_group(groupname="Test Group")
        the_group.save()
        the_gallery = gus_gallery.objects.create(group=the_group, user=the_user, name="Test Gallery")
        the_gallery.save()

        # If either the user or the group isn't set, then fail the test
        self.failIfEqual(the_user, None, "Could not initialize test user.")
        self.failIfEqual(the_group, None, "Could not initialize test group.")
        self.failIfEqual(the_gallery, None, "Could not initialize test gallery.")

        ## TEST 1 - Create an image, add it to the gallery
        the_image = gus_image.objects.create(gallery=the_gallery, user=the_user, image_path="/img/blah.jpg")
        the_image.save()
        self.failIfEqual(the_image, None, "Could not initialize test image.")

        the_gallery.add_image(the_image)
        self.failUnlessEqual(the_image.gallery, the_gallery, "Image not added to gallery.")


    def test_get_images(self):
        """
        Tests the gus_gallery.get_images() method
        """
        # TODO: Implement the test


    def test_num_images(self):
        """
        Tests the gus_gallery.num_images() method
        """
        # TODO: Implement the test
