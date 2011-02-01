"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import unittest
from src.gus2.gus_calendar.models import Calendar
from src.gus2.gus_calendar.models import Event

class Calendar_test(unittest.TestCase):
    def basic_test(self):
        self.name = Calendar.name = "Group Calendar"
        self.date = Calendar.current_date
#        self.failUnlessEqual(1 + 1, 2)
        print "WIN"

class Event_test(unittest.TestCase):
        def basic_test(self):
            self.calendar = Event.calendar
            self.id = 5
            self.group_id = Event.group_id(25)
            self.event_name = Event.event_name("Spock's Birthday")
            self.start_date = "10/31/2010"
            self.end_date = "11/13/2010"
            print "WIN"

