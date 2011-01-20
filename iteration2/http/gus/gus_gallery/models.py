# Gus Gallery Models
# Part of the GUSPY effort
# Stephen Fischer
# January 2011
#
# TODO: Figure out where to actually save image files, update the gus_image class to reflect that
# TODO: See if I'm doing the gus_image queries right in gus_gallery.get_images and gus_gallery.delete

from django.db import models
from gus.gus_groups.models import *

class gus_gallery(models.Model):
    """
    An image gallery belonging to a gus_group.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(gus_groups)
    name = models.CharField(500)
    user = models.ForeignKey(gus_users)

    def __unicode__(self):
        """
        When referencing the gallery object, return its name.
        
        @rtype: string
        @return: The name of the gallery.
        """
        return self.name;

    def delete(self):
        """
        Deletes the gallery and all the images associated with it.
        """
        for i in self.gus_image_set:
            i.delete()
        super(gus_gallery, self).delete()

    def add_image(self, img):
        """
        Adds a given image to the gallery.
        """
        img.gallery = self
        img.save()

    def get_images(self):
        """
        Gets an array of images that belong to the gallery.
        
        @rtype: gus_image[]
        @return: An array of images in the gallery.
        """
        try:
            return self.gus_image_set.filter(galery_id=self)
        except:
            return None


class gus_image(models.Model):
    """
    A single image belonging to a gus_gallery.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    gallery = models.ForeignKey(gus_gallery)
    image_path = models.CharField(500)
    user = models.ForeignKey(gus_users)

    def __unicode__(self):
        """
        When referencing the image object, return its URL path.

        @rtype: string
        @return: The path to the image file on the server.
        """
        return self.image_path

    def delete(self):
        """
        Deletes the image in the database and from the file system.
        """
        try:
            os.remove(self.image)
        except:
            pass
        super(gus_image, self).delete()
