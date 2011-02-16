# GUS Gallery Model Tests
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
    def test_gallery(self):
        """
        Tests the gus_gallery object to see if it can be initialized/deleted
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
        the_gallery.save()
        self.failIfEqual(the_gallery, None, "Could not initialize test gallery.")

        gallery_count_before = len(gus_gallery.objects.all())

        ## TEST 2 - Delete the valid gallery
        the_gallery.delete()

        gallery_count_after = len(gus_gallery.objects.all())
        self.failIfEqual(gallery_count_before, gallery_count_after, "Could not delete test gallery.")

        ## TEST 3 - Try to create incomplete galleries, fail if they work
        try:
            the_gallery = gus_gallery.objects.create(group=None, user=the_user, name="Test Gallery 2")
            the_gallery.save()
            self.failUnlessEqual(the_gallery, None, "Created invalid gallery without a group.")
        except:
            # Do nothing
            the_gallery = None
        try:
            the_gallery = gus_gallery.objects.create(group=the_group, user=None, name="Test Gallery 3")
            the_gallery.save()
            self.failUnlessEqual(the_gallery, None, "Created invalid gallery without a user.")
        except:
            # Do nothing
            the_gallery = None
        try:
            the_gallery = gus_gallery.objects.create(group=None, user=None, name="Test Gallery 4")
            the_galelry.save()
            self.failUnlessEqual(the_gallery, None, "Created invalid gallery without a group or user.")
        except:
            # Do nothing
            the_gallery = None


    def test_image(self):
        """
        Tests the gus_image objects to see if it can be initialized/deleted/manipulated
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

        ## TEST 1 - Create an image
        the_image = gus_image.objects.create(gallery=the_gallery, user=the_user, image_path="/img/blah.jpg")
        the_image.save()
        self.failIfEqual(the_image, None, "Could not initialize test image.")

        ## TEST 2 - Add the image to a gallery
        the_gallery.add_image(the_image)
        self.failUnlessEqual(the_image.gallery, the_gallery, "Could not add image to gallery.")

        ## TEST 3 - Test the gus_gallery.num_images() function
        count = the_gallery.num_images()
        self.failUnlessEqual(count, 1, "the_gallery.num_images() Failed. Expected 1, Got %d." % (count))

        ## TEST 4 - Test the gus_gallery.get_images() function
        self.failUnlessEqual(the_image, the_gallery.get_images()[0], "the_gallery.get_images() Failed.")

        ## TEST 5 - Delete the image
        num_images_old = len(gus_image.objects.all())
        the_image.delete()
        num_images_new = len(gus_image.objects.all())
        self.failIfEqual(num_images_old, num_images_new, "Could not delete test image.")
