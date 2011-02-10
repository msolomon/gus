from django.db import models
from gus2.gus_widget.models import Widget #ok
from gus2.gus_users.models import gus_user #ok ignore aptana

class gus_calendar(Widget):
    """
    An calendar belonging to a gus_group.
    """
    current_date = models.DateField(auto_now=True)
    #name inherited from Widget

    def __unicode__(self):
        """return name inherited from Widgit
        @return: name of calendar. type string
        """
        return self.name 

    def get_events(self):
            return gus_event.objectsfilter(calendar_id=self)
        
    def add_event(self, event):
        event.calendar = self
        event.save()
        
    def delete_calendar(self):
        events = self.get_events()
        for event in events:
            event.delete() ##or event.delete()
            ##  super(gus_calendar, self).delete()
        self.delete()
          
class gus_event(models.Model):
    """
    An event for a gus_calendar belonging to a gus_group.
    """
    # use foreign key for Calendar to show many-to-one relationship
    calendar = models.ForeignKey(gus_calendar)
    event_id = models.IntegerField()
    group_id = models.IntegerField()
    event_name = models.CharField(max_length=60)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    description = models.CharField(max_length=250, blank=True)
    creator = models.ForeignKey(gus_user, blank=True, null=True)
    #reminder = models.BooleanField(default=False)
    
    def __unicode__(self):
        if self.event_name:
            return unicode(self.event_name) + " : " + self.creator
        else:
            return unicode(self.creator) + " : " + self.description[:40]

    def delete_event(self):
        self.delete()
        ##super(gus_event, self).delete()
