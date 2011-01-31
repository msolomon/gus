"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from gus_calendar.models import Calendar
from gus_calendar.models import Calendar_item

class Calendar_test(TestCase):
    def basic_test(self):
        self.name = Calendar.name = "Group Calendar"
        self.date = Calendar.current_date
#        self.failUnlessEqual(1 + 1, 2)

class Calendar_item_test(TestCase):
        def basic_test(self):
            self.calendar = calendar
            self.id = 5
            self.group_id = 25
            self.name = "Event"
            self.start = "10/31/2010"


