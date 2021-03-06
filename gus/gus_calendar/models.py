"""
Guspy gus implementation
Gus_Calendar and Gus_Event Classes
Sasha Kopriva

This is the model document for the Gus_calendar and Gus_event classes. 

"""

from django.db import models
from gus.gus_widget.models import Widget #ok
from gus.gus_users.models import gus_user #ok ignore aptana
from gus.gus_groups.models import gus_group
from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import Select
from gus.gus_groups.utils import *

valid_time_formats = ['%P', '%H:%M%A', '%H:%M %A', '%H:%M%a', '%H:%M %a']
class Gus_calendar(Widget):
    """
    An calendar belonging to a gus_group.
    
    """
    current_date = models.DateField(auto_now=True)
    #name inherited from Widget

    def __unicode__(self):
        """
        Returns the name of the calendar.
        @rtype: string
        @return: name of calendar
        
        """
        return self.name 
        
    def add_event(self, event):
        """
        Adds an event to the calendar.
        
        """
        event.calendar = self
        event.save()
          
class Gus_event(models.Model):
    """
    An event for a gus_calendar belonging to a gus_group.
    
    """

    auth_groups= []
    event_name = models.CharField(max_length=60)
    start_date = models.DateField(blank=True)
    description = models.CharField(max_length=1000, blank=True)
    creator = models.ForeignKey(gus_user, blank=True, null=True)
    Delete = models.BooleanField(blank=True, null=False)
    Group = models.ForeignKey(gus_group, null=True)
    start_time = models.TimeField(help_text='Ex: 13:00')
    end_time = models.TimeField(help_text='Ex: 13:00')
    #Attending = models.BooleanField(blank=True, null=False)
    #reminder = models.BooleanField(default=False)
    
    def __unicode__(self):
        """
        Returns the name of the event and its creator OR if there is no event name,
        Returns the creator and a snippet of the event's description.
        @rtype: string
        @return: name of event and its creator OR creator and snippet of event's description.
        
        """
        ## no gus users created yet
        if self.event_name:
            return unicode(self.event_name) #+ " : " ## + self.creator
        ##else:
         ##   return unicode(self.creator) + " : " + self.description[:40]

    def delete_event(self):
        """
        Deletes the event.
        
        """
        self.delete()


class Event_form(ModelForm):         
    class Meta:
        model = Gus_event
        exclude = ('start_date', 'creator')
        fields = ('event_name', 'description', 'Group', 'start_time', 'end_time')
        
class Event_form_edit(ModelForm):
    class Meta:
        model = Gus_event
        exclude = ('start_date', 'creator',)
        fields = ('event_name', 'description', 'start_time','end_time', 'Delete')
        
#class Event_form_userview(ModelForm):
#    class Meta:
#        model = Gus_event
#        exclude = ('start_date', 'creator',)
#        fields = ('event_name', 'description', 'Attending')