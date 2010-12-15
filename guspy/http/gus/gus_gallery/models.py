from django.db import models

# The image gallery model
class gus_gallery(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(gus_group)
    name = models.TextField()
    user = models.ForeignKey(gus_user)
    
    def __unicode__(self):
        return self.name
        
# The image model
class gus_image(models.Model):
    date_created = models.DateTimeFiels(auto_now_add=True)
    file = models.ImageField(upload_to='images/%Y/%m')
    gallery = models.ForeignKey(gus_gallery)
    user = models.ForeignKey(gus_user)

    def __unicode__(self):
        return self.file
