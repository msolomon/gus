# GUS Gallery Models
# Part of the GUSPY effort
# Stephen Fischer
# January 2011
#
# TODO: Create a smarter gus_gallery.delete() that will delete all the associated images
#   at the same time.

from django.db import models
from django.forms import ModelForm
from gus.gus_groups.models import *
from gus.gus_users.models import *

class gus_gallery(models.Model):
    """
    An image gallery belonging to a gus_group.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(gus_group)
    name = models.CharField(max_length=500)
    user = models.ForeignKey(gus_user)
    is_public = models.BooleanField()

    def __unicode__(self):
        """
        When referencing the gallery object, return its name.
        
        @rtype: string
        @return: The name of the gallery.
        """
        return self.name;

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
            return gus_image.objects.filter(gallery=self)
        except:
            return None

    def num_images(self):
        """
        Returns the number of images in the gallery
        """
        try:
            return len(get_images())
        except:
            return 0


class gus_image(models.Model):
    """
    A single image belonging to a gus_gallery.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    gallery = models.ForeignKey(gus_gallery)
    image = models.ImageField(upload_to='gallery/%Y/%m')
    name = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(gus_user)
    
    def __unicode__(self):
        """
        When referencing the image object, return its URL path.

        @rtype: string
        @return: The path to the image file on the server.
        """
        return self.name

    def delete(self):
        """
        Deletes the image in the database and from the file system.
        """
        try:
            os.remove(self.image)
        except:
            pass
        super(gus_image, self).delete()


class gallery_form(ModelForm):
    """
    The basic form for a gus_gallery
    """
    class Meta:
        model = gus_gallery
        fields = ('name', 'is_public')

class image_form(ModelForm):
    """
    The basic form for a gus_image
    """
    class Meta:
        model = gus_image
        fields = ('image',
                  'name',
                  'description')

class image_edit_form(ModelForm):
    """
    The basic form for editing a gus_image
    """
    class Meta:
        model = gus_image
        fields = ('name',
                  'description')
