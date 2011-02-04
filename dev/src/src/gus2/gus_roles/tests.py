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
    """
    class SimpleTest Tests the core functionality of the roles
    namely the creation /editing/ deletion of roles
    """
    testRole ='testRole'
    testGroup=None
    testUser1=None
    testUser2=None
    def setUp(self):
        """
        setup a group and a couple users to use with role tests
        @requires: L{gus_group.create_group<gus2.gus_groups.models.GroupManager.create_group>}
        @requires: L{gus_user.create_user<gus2.gus_users.models.UserManager.create_user>}
        """
        self.testGroup = gus_group.objects.create_group("TestGroup1", "Added For Testing Roles", '')
        self.testUser1  = gus_user.objects.create_user("Test User1", "test@user1", '1')
        self.testUser2  = gus_user.objects.create_user("Test User2", "test@user2", '2')
        
    def test_createAndDelete_role(self):
        """
    	@summary:  tests that roles can be created
    	
    	@precondition: L{setUp} 
    	
    	tests built in django model deletion 
    	and L{gus_role.create_role<gus2.gus_roles.models.RoleManager.create_role>} 
    	"""
        print "Test Create Role test_roles"  
        group_object = gus_group.objects.create_group('test_roles', 'test', '')
        gus_role.objects.create_role(group_object, 'test_role')
        role = gus_role.objects.get(_role_name='test_role')
        self.failUnlessEqual(role._role_name, 'test_role','RoleCreationError:Could Not Create Role')
        





