"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    testGroupName = "test_group_420"
    
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

    def test_basic_groupCreate(self):
        """
        tests that a group can be created successfully
        """
        print "Test Create Group %s" % self.testGroupName        
        from gus2.gus_groups.models  import gus_group
        gus_group.objects.create_group(self.testGroupName, 'unit test created','')
        grp = gus_group.objects.get(group_name=self.testGroupName)
        self.failUnlessEqual(grp.group_name, self.testGroupName)
    
        