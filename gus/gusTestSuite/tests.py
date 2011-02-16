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
    testGroupName2 = "group_of_failures" # [JS]
    testRoleName = 'test_role_grunt'
    testRoleName2 = 'test_role_bigcheese'
    testRoleName3 = 'test_role_obama' # [JS]
    testUserName = 'grunt1'
    testUserName2 = 'grunt2'
    def test_basic_groupCreateManageUser(self):
        """
        tests that users can be added and deleted to a group
        tests functionality of 
        """      
        
        #Create a test group to hang all of our tests on
        gus_group.objects.create_group(self.testGroupName, 'unit test created', '')
        grp = gus_group.objects.filter(group_name=self.testGroupName)
        #simple test to make sure group created properly; do we need since this is tested elsewhere?
        self.failUnlessEqual(grp[0].group_name, self.testGroupName)
        
        #Create a secondary group to test addition of users to other groups
        gus_group.objects.create_group(self.testGroupName2, 'unit test created', '')
        grp2 = gus_group.objects.filter(group_name=self.testGroupName2)
        #Make sure this created properly too.
        self.failUnlessEqual(grp2[0].group_name, self.testGroupName2)
        
        #Create a test role and make sure that initializes properly
        gus_role.objects.create_role(grp[0], self.testRoleName)
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
        self.failUnlessEqual(len(gus_role.objects.users_with_group(grp)), 2, 'Incorrectly adding users to group')
        
        #Now we see if a user can be added to more than one role
        #This necessitates creating a second role
        gus_role.objects.create_role(grp[0], self.testRoleName2)
        role2 = gus_role.objects.filter(_role_name=self.testRoleName2)
        #Test to make sure a second role adds to the group as easily as the first
        self.failUnlessEqual(len(gus_role.objects.with_group(grp)), 2, 'Group failed to recognize role')
        #Now we try and elevate grunt1 to bigcheese status
        role2[0].addUser(usr)
        #Make sure that we still only have 2 users counted as being in the group
        self.failUnlessEqual(len(gus_role.objects.users_with_group(grp)), 2, 'Incorrectly adding users to group')
        #Check to see if usr now has two roles
        self.failUnlessEqual(len(gus_role.objects.with_user(usr)), 2, 'Failed to correctly assign multiple roles')
        self.failUnlessEqual(len(gus_role.objects.with_user(usr2)), 1, 'Failed to correctly assign multiple roles')
        
        #Now see if users can be part of multiple roles and groups [JS]
        gus_role.objects.create_role(grp2[0], self.testRoleName3)
        role3 = gus_role.objects.filter(_role_name=self.testRoleName3)
        
        self.failUnlessEqual(len(gus_role.objects.with_group(grp2)), 1, 'Group failed to recognize role [grp2]')
        
        role3[0].addUser(usr)
        
        self.failUnlessEqual(len(gus_role.objects.users_with_group(grp2)), 1, 'User is not (or too many users) in [grp2]')
        self.failUnlessEqual(len(gus_role.objects.with_user(usr)), 3, 'User is in incorrect number of roles')
        
        #Test deletion of usr from the group, thus sadly eliminating our only bigcheese
        #NOTE: I do NOT see a way of listing all members with a given role.
        #      I see all members of a group, and all roles of a group, and all roles of a user
        #      This prevents me from running a test on each role, which I would like to ~ Nathan
        
        #NOTE: I've figured out a "safe" way to do this: by first removing a user from the role, you can
        #      look to see if the user is still in the role.  After that, it _will_ be safe to delete the
        #      user and assume the user is gone from the role as well. [JS 2011-02-10]
        #      This also tests the role delete-user function, though it is likely tested elsewhere.
        #gus_role.objects.users_with_group(some_group)  will return all users of a group ~joran
        #Remove the user from roles
        role[0].removeUser(usr)
        role2[0].removeUser(usr)
        role3[0].removeUser(usr)
        self.failUnlessEqual(len(gus_role.objects.with_user(usr)), 0, 'User is still in groups!')
        #Now delete the user
        usr.delete()
        self.failUnlessEqual(len(gus_role.objects.users_with_group(grp)), 1, 'Incorrectly deleted user from group')
        
        
        return 1
    

