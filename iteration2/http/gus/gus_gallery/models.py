# Gus Gallery Models
# Part of the GUSPY effort
# Stephen Fischer
# January 2011
#
# TODO: Figure out where to actually save image files, update the gus_image class to reflect that

from django.db import models
from gus.gus_groups.models import *

class gus_gallery(models.Model):
    """
    An image gallery belonging to a gus_group
    """
    date_created = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(gus_groups)
    name = models.CharField(500)
    user = models.ForeignKey(gus_users)

    def delete(self):
        """
        Deletes the gallery and all the images associated with it
        """
        for i in self.gus_image_set:
            i.delete()
        super(gus_gallery, self).delete()

    def add_image(self, img):
        """
        Adds a given image to the gallery
        """
        img.gallery = self
        img.save()

class gus_image(models.Model):
    """
    A single image belonging to a gus_gallery
    """
    date_created = models.DateTimeField(auto_now_add=True)
    gallery = models.ForeignKey(gus_gallery)
    image = models.ImageField(upload_to="images/%Y/%m")
    user = models.ForeignKey(gus_users)

    def delete(self):
        """
        Deletes the image in the database and from the file system
        """
        try:
            os.remove(self.image)
        except:
            pass
        super(gus_image, self).delete()
