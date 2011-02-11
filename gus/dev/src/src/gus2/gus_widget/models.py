from django.db import models
from gus2.gus_groups.models import gus_group

class Widget(models.Model):
    """
    class Widget model is the base model for any gus plug-in
    
    Examples of widget "plug-ins"  are calenders, image galleries,
    forums, and other optional group functionality.  These widgets
    should have foreign keys to this class.
    """
    
    ### Fields
    
    # as i understand, a primary key will be set up automatically
    # which should suffice for the ID
    group = models.ForeignKey(gus_group)
    name = models.CharField(max_length=32)
    # is the widget enabled in the current group?
    enabled = models.BooleanField()
    
    
    # the permissions class doesn't exist, but it should
    #permissions = models.ForeignKey(permissions)
    
    ### Magic Functions
        
    def __unicode__(self):
        """
        The default string representation of a Widget.
        
        @rtype: string
        @return:    The name of the widget
        """
        
        return self.name
    
    
