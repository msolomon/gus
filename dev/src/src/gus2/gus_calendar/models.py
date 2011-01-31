from django.db import models
from gus2.gus_widget.models import Widget
from gus2.gus_users.models import User
class Calendar(Widget):
    """
    class Calendar is a widget and inherits from the Widget class.
    This class is also related to Calendar_item as many 
    Calendar_items are related to a single Calendar.
    """
    name = models.CharField(max_length=32)
    current_date = models.DateField(auto_now=True)
    
  
class Calendar_item(models.Model):
    """
    class Calendar_item inherits from models.Model and is related to the 
    Calendar class as Calendar_items are related to a single 
    Calendar (using a ForeignKey)
    """
    # use foreign key for Calendar to show many-to-one relationship
    calendar = models.ForeignKey(Calendar)
    
    id = models.IntegerField()
    group_id = models.IntegerField()
    
    
    event_name = models.CharField(max_length=60)
    # start date for a calendar event
    start = models.DateTimeField('start date')
    #end date for a calendar event
    end = models.DateTimeField('end date')
    description = models.CharField(max_length=250, blank=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    
    def __unicode__(self):
        if self.event_name:
            return unicode(self.event_name) + " : " + self.creator
        else:
            return unicode(self.creator) +  " : " + self.description[:40]
