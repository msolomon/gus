from django.db import models
from gus2.gus_widget.models import Widget #ok
from gus2.gus_users.models import gus_user #ok ignore aptana

class Calendar(Widget):
    """
    class Calendar is a widget and inherits from the Widget class.
    This class is also related to Calendar_item as many 
    Calendar_items are related to a single Calendar.
    """
    current_date = models.DateField(auto_now=True)
    #name inherited from Widget
  
class Event(models.Model):
    """
    class Calendar_item inherits from models.Model and is related to the 
    Calendar class as Calendar_items are related to a single 
    Calendar (using a ForeignKey)
    """
    # use foreign key for Calendar to show many-to-one relationship
    
    
    calendar = models.ForeignKey(Calendar)
    
    event_id = models.IntegerField()
    group_id = models.IntegerField()
    
    
    event_name = models.CharField(max_length=60)
    #-- start date for a calendar event
    start_date = models.DateTimeField(blank=True)
    #-- end date for a calendar event
    end_date = models.DateTimeField(blank=True)
    description = models.CharField(max_length=250, blank=True)
    creator = models.ForeignKey(gus_user, blank=True, null=True)
    #reminder = models.BooleanField(default=False)
    def __unicode__(self):
        if self.event_name:
            return unicode(self.event_name) + " : " + self.creator
        else:
            return unicode(self.creator) + " : " + self.description[:40]
