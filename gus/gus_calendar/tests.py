"""
Guspy gus implementation
Gus_Calendar and Gus_Event Tests
Sasha Kopriva


This is a test document for the Gus_calendar and Gus_event classes. It tests 
basic functionality of both classes.

"""

from django.test import TestCase
import unittest

from gus_calendar.models import Gus_calendar #ok ignore aptana
from gus_calendar.models import Gus_event #ok ignore aptana
from gus.gus_users.models import *
from gus.gus_groups.models import *


class test_gus_calendar(unittest.TestCase):
    def test_calendar_init(self):
        new_user = gus_user.objects.create_user(username="Mr. Spock", email="enterprise@gmail.com", password="queentoqueenslevel3")
        new_user.save()
        new_group = gus_group.objects.create_group(groupname="USS Enterprise Officers")
        new_group.save()
        
        self.failIfEqual(gus_user.objects.filter(pk=new_user.id), None, "gus_user object not initialized.")
        self.failIfEqual(gus_group.objects.filter(group_name=new_group.group_name), None, "gus_group object not initialized.")
        
        ## user not included in Widget class, thus not included in calendar creation
        new_calendar = Gus_calendar.objects.create(group = new_group, name = "Enterprise Calendar")
        new_calendar.save()
        self.failIfEqual(Gus_calendar.objects.filter(name=new_calendar.name), None, "Gus_calendar object not initialized.") 
        print "\ngus_calendar test_calendar_init: pass"

class test_gus_event(unittest.TestCase):    
        def test_event_init(self):
            
            new_user = gus_user.objects.create_user(username="Spock", email="enterprise@gmail.com", password="queentoqueenslevel3")
            new_user.save()
            self.failIfEqual(new_user, None, "gus_user object not initialized.")
            
            new_group = gus_group.objects.create_group(groupname="USS Enterprise Crew")
            new_group.save()
            self.failIfEqual(gus_group.objects.filter(group_name=new_group.group_name), None, "gus_group object not initialized.")
            
            ## user not included in Widget class, thus not included in calendar creation
            new_calendar = Gus_calendar.objects.create(group = new_group, name = "Enterprise Calendar") 
            new_calendar.save()
            self.failIfEqual(Gus_calendar.objects.filter(name=new_calendar.name), None, "Gus_calendar object not initialized.")        

            event_description = "Mission to acquire a Valentine for Spock."
            

            new_event = Gus_event.objects.create(creator = new_user, 
                                                 event_name = "Mission 1", 
                                                 start_date = "2011-02-14",
                                                 start_time = "10:00:00",
                                                 end_time = "14:00:00", 
                                                 description = event_description,
                                                 Group = gus_group.objects.get(group_name="USS Enterprise Crew"))
            new_event.save()
            self.failIfEqual(Gus_event.objects.filter(event_name=new_event.event_name),
                              None,
                               "Gus_event object not initialized.")
            print "\ngus_calendar test_event_init: pass"

