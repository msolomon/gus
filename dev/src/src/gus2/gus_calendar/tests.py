"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import unittest

from gus_calendar.models import Calendar #ok ignore aptana
from gus_calendar.models import Event #ok ignore aptana
from gus2.gus_users.models import *
from gus2.gus_groups.models import *


class test_gus_calendar(unittest.TestCase):
    def test_calendar_init(self):
        new_user = gus_user.objects.create_user(username="Spock", email="enterprise@gmail.com", password="queentoqueenslevel3")
        new_user.save()
        new_group = gus_group.objects.create_group(group_name="USS Enterprise Crew")
        new_group.save()
        
        self.failIfEqual(new_user, None)
        self.failIfEqual(new_group,None)
        
        new_calendar = gus_calendar.objects.create(group = new_group, user = new_user, name = "Enterprise Calendar")
        new_calendar.save()
        self.failIfEqual(new_calendar, None)
        
        new_calendar.delete_calendar()
        self.failUnlessEqual(new_calendar, None)
        
        new_calendar.get_events()
        self.failIfEqual(new_calendar, None)

        new_calendar = gus_calendar.objects.create(group = None, user = new_user, name = "Calendar 1")
        self.failUnlessEqual(new_calendar, None)
        
        new_calendar = gus_calendar.objects.create(group = new_group, user = None, name = "Calendar 2")
        self.failUnlessEqual(new_calendar, None)
        
        new_calendar = gus_calendar.objects.create(group = None, user = None, name = "Calendar 3")
        self.failUnlessEqual(new_calendar, None)

        new_calendar.delete_calendar()
        self.failUnlessEqual(new_calendar, None)
        
        print "\ngus_calendar test_calendar_init: pass"

class test_gus_event(unittest.TestCase):    
        def test_event_init(self):
            
            new_user = gus_user.objects.create_user(username="Spock", email="enterprise@gmail.com", password="queentoqueenslevel3")
            new_user.save()
            self.failIfEqual(new_user, None)
            
            new_group = gus_group.objects.create_group(group_name="USS Enterprise Crew")
            new_group.save()
            self.failIfEqual(new_group,None)
            
            new_calendar = gus_calendar.objects.create(group = new_group, user = new_user, name = "Enterprise Calendar")
            new_calendar.save()
            self.failIfEqual(new_calendar,None)        

            event_description = "Mission to acquire a Valentine for Spock."
            
            new_event = gus_event.create(calendar = new_calendar, creator = new_user, event_name = "Mission 1", start_date = "02/14/2011", end_date = "02/15/2011", description = event_description)
            new_event.save()
            self.failIfEqual(new_event, None)
        
            new_calendar.add_event(new_event)
            events = new_calendar.get_events()
            self.failIfEqual(events, None)
            
            new_event.delete_event()
            self.failUnlessEqual(new_event, None)
            
            new_event = gus_event.create(calendar = None, creator = new_user, event_name = "Failed Mission 1", start_date = "02/14/2011", end_date = "02/15/2011", description = event_description)
            self.failUnlessEqual(new_event, None)
            
            new_event = gus_event.create(calendar = new_calendar, creator = None, event_name = "Failed Mission 2", start_date = "02/14/2011", end_date = "02/15/2011", description = event_description)
            self.failUnlessEqual(new_event, None)
            
            new_event = gus_event.create(calendar = None, creator = None, event_name = "Failed Mission 1", start_date = "02/14/2011", end_date = "02/15/2011", description = event_description)
            self.failUnlessEqual(new_event, None)
            

