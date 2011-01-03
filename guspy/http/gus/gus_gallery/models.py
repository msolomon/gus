# Part of the GUSPY effort
# Stephen Fischer
# January 2011
 
from django.db import models
from gus.gus_groups.models import *

# The class representing an image gallery
class gus_gallery(models.Model):
    group = models.ForeignKey(gus_groups)
    name = models.CharField(500)

# The class representing an image inside a gallery
class gus_image(models.Model):
    gallery = models.ForeignKey(gus_gallery)
    user = models.ForeignKey(gus_users)
