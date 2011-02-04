"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from gus2.gus_groups.models import gus_group
from gus2.gus_roles.models import gus_role
from gus2.gus_users.models import gus_user

class SimpleTest(TestCase):
    testGroupName = "test_group_suite"
    testRoleName = 'test_role_grunt'
    testRoleName2 = 'test_role_bigcheese'
    testUserName = 'grunt1'
    testUserName2 = 'grunt2'
    def test_basic_groupCreateManageUser(self):
        """
        tests that users can be added and deleted to a group
        tests functionality of 
        """
        print "Test Create Group %s" % self.testGroupName        
        
        #Create a test group to hang all of our tests on
        gus_group.objects.create_group(self.testGroupName, 'unit test created','')
        grp = gus_group.objects.filter(group_name=self.testGroupName)
        #simple test to make sure group created properly; do we need since this is tested elsewhere?
        self.failUnlessEqual(grp[0].group_name, self.testGroupName)
        
        
        #Create a test role and make sure that initializes properly
        gus_role.objects.create_role(grp[0],self.testRoleName)
        role = gus_role.objects.filter(_role_name=self.testRoleName)
        #Test to make sure the role was created
        self.failUnlessEqual(role[0]._role_name, self.testRoleName, 'Failed to create role')
        #Test to make sure that the group recognizes the role
        self.failUnlessEqual(len(gus_role.objects.with_group(grp)), 1, 'Group failed to recognize role')
        
        #Create two test users and test to make sure they exist
        usr = gus_user.objects.create_user(self.testUserName, 'email', 'password');
        self.failUnlessEqual(usr.username, self.testUserName, 'Failed to create user')
        usr2 = gus_user.objects.create_user(self.testUserName2, 'email', 'password');
        self.failUnlessEqual(usr2.username, self.testUserName2, 'Failed to create user')
        
        
        #Now we see if we can attach the users to a role
        role[0].addUser(usr)
        role[0].addUser(usr2)
        print "Users in group: %s" % gus_role.objects.users_with_group(grp)
        self.failUnlessEqual(len(gus_role.objects.users_with_group(grp)), 2, 'Incorrectly adding users to group')
        
        #Now we see if a user can be added to more than one role
        #This necessitates creating a second role
        gus_role.objects.create_role(grp[0],self.testRoleName2)
        role2 = gus_role.objects.filter(_role_name=self.testRoleName2)
        #Test to make sure a second role adds to the group as easily as the first
        self.failUnlessEqual(len(gus_role.objects.with_group(grp)), 2, 'Group failed to recognize role')
        #Now we try and elevate grunt1 to bigcheese status
        role2[0].addUser(usr)
        print "The many roles of grunt1: %s" % gus_role.objects.with_user(usr)
        #Make sure that we still only have 2 users counted as being in the group
        self.failUnlessEqual(len(gus_role.objects.users_with_group(grp)), 2, 'Incorrectly adding users to group')
        #Check to see if usr now has two roles
        self.failUnlessEqual(len(gus_role.objects.with_user(usr)), 2, 'Failed to correctly assign multiple roles')
        self.failUnlessEqual(len(gus_role.objects.with_user(usr2)), 1, 'Failed to correctly assign multiple roles')
        
        #Test deletion of usr from the group, thus sadly eliminating our only bigcheese
        #NOTE: I do NOT see a way of listing all members with a given role.
        #      I see all members of a group, and all roles of a group, and all roles of a user
        #      This prevents me from running a test on each role, which I would like to ~ Nathan
        usr.delete()
        self.failUnlessEqual(len(gus_role.objects.users_with_group(grp)), 1, 'Incorrectly deleted user from group')
        
        
        return 1
    

