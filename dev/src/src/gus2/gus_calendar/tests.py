"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import unittest
from gus_calendar.models import Calendar #ok ignore aptana
from gus_calendar.models import Event #ok ignore aptana

class Calendar_test(unittest.TestCase):
    def basic_test(self):
        calendar = Calendar()
        #self.name = Calendar.name = "Group Calendar"
        #self.failUnlessEqual(1 + 1, 2)
        print "gus_calendar: pass"

class Event_test(unittest.TestCase):    
        def basic_test(self):
            event_id = 0001
            group_id = 1  
            event = Event()
            event.event_id = event_id
            event.group_id = group_id
##            self.calendar = Event.calendar
##            self.id = 5
##           self.group_id = Event.group_id(25)
##            self.event_name = Event.event_name("Spock's Birthday")
##            self.start_date = "10/31/2010"
##            self.end_date = "11/13/2010"
            self.failUnlessEqual(event_id, event.event_id)
            self.failUnlessEqual(group_id, event.group_id)
            print "gus_calendar: pass"

