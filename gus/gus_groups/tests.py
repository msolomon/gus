"""
This File Tests the Functionality of the gus_group module
for the python implementation of guspy

"""

from django.test import TestCase
from django.db import IntegrityError
from gus.gus_groups.models import gus_group
from gus.gus_users.models import gus_user
from gus.gus_roles.models import gus_role
from gus.gus_groups.utils import createNewGroup


class GusGroupTest(TestCase):
    """
    This class shall test the core functionality of the 
    gus_group module
    """
    testGroupName = "test_group"
    
    def setUp(self):
        self.test_user = gus_user.objects.create_user("test","test2","test3")
        self.test_user1 = gus_user.objects.create_user("testMember","test2","test3")
    def test_basic_groupCreateDelete(self):
        """
        tests that a group can be created successfully
        uses Django's built in delete() functionality for models
        tests functionality of L{gus_group.create_group<gus.gus_groups.models.GroupManager.create_group>}
        """      
        gus_group.objects.create_group(self.testGroupName, 'unit test created', '')
        grp = gus_group.objects.filter(group_name=self.testGroupName)
        self.failUnlessEqual(grp[0].group_name, self.testGroupName)
        
        grp.delete()
        self.failUnlessEqual(len(gus_group.objects.filter(group_name=self.testGroupName)), 0, 'failed to delete test group')
        
    def test_advanced_groupCreate(self):
        """
        tests that trying to create a group with the same name as an existing one will fail
        tests functionality of L{gus_group.create_group<gus.gus_groups.models.GroupManager.create_group>}
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
        tests functionality of L{gus_group.create_group<gus.gus_groups.models.GroupManager.create_group>}
        """
        gus_group.objects.create_group(self.testGroupName, 'test group', '')
        grp = gus_group.objects.filter(group_name=self.testGroupName)
        
        self.failUnlessEqual(len(grp) > 0, True, 'Unable to create group')
        grp[0].group_description = "Altered Description"
        grp[0].save()
        grp = gus_group.objects.filter(group_name=self.testGroupName)
        self.failUnlessEqual("Altered Description", grp[0].group_description, 'Unable to edit group description')
        
    def test_abstract_group_creation(self):
        """
        Tests the functionality of gus_groups.utility.createNewGroup
        Helper, as well as gus_group.addUser
        """
        grp = createNewGroup(self.test_user,self.testGroupName,"asd","")
        grp.addUser(self.test_user1)
        try:
            testRole=self.test_user1.roles[0]
            self.failUnless(testRole._role_name=="Member" or testRole._role_group==grp,
                            "gus_group.addUser Failure")
        except:
            self.fail("No Role Found For User,Should have a role")
