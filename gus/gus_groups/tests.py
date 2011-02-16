"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

This tests general group functionality

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.db import IntegrityError
from gus2.gus_groups.models import gus_group

class SimpleTest(TestCase):
    testGroupName = "test_group"

    def test_basic_groupCreateDelete(self):
        """
        tests that a group can be created successfully
        uses Django's built in delete() functionality for models
        tests functionality of L{gus_group.create_group<gus2.gus_groups.models.GroupManager.create_group>}
        """      
        gus_group.objects.create_group(self.testGroupName, 'unit test created', '')
        grp = gus_group.objects.filter(group_name=self.testGroupName)
        self.failUnlessEqual(grp[0].group_name, self.testGroupName)
        
        grp.delete()
        self.failUnlessEqual(len(gus_group.objects.filter(group_name=self.testGroupName)), 0, 'failed to delete test group')
        
    def test_advanced_groupCreate(self):
        """
        tests that trying to create a group with the same name as an existing one will fail
        tests functionality of L{gus_group.create_group<gus2.gus_groups.models.GroupManager.create_group>}
        """
        gus_group.objects.create_group(self.testGroupName, 'initial group created', '')
        grp = gus_group.objects.filter(group_name=self.testGroupName)
        
        try:
            gus_group.objects.create_group(self.testGroupName, 'secondary group created', '')
        except IntegrityError:
            return
        #If we get here, we created two groups with the same name, which is bad
        #We should have exited by now by getting an integrity error above
        self.failUnlessEqual(1, 2, 'Created two identical User Group Names')
        
        
    def test_edit_group(self):
        """
        tests trying to edit the description of a group
        tests functionality of L{gus_group.create_group<gus2.gus_groups.models.GroupManager.create_group>}
        """
        gus_group.objects.create_group(self.testGroupName, 'test group', '')
        grp = gus_group.objects.filter(group_name=self.testGroupName)
        
        self.failUnlessEqual(len(grp) > 0, True, 'Unable to create group')
        grp[0].group_description = "Altered Description"
        grp[0].save()
        grp = gus_group.objects.filter(group_name=self.testGroupName)
        self.failUnlessEqual("Altered Description", grp[0].group_description, 'Unable to edit group description')
        
        
        
