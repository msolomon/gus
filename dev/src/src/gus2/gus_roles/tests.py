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
        group_object = gus_group.objects.create_group(self.testRole, 'test', '')
        #Test Creation
        gus_role.objects.create_role(group_object, self.testRole)
        role = gus_role.objects.get(_role_name=self.testRole)
        self.failUnlessEqual(role._role_name, self.testRole,'RoleCreationError:Could Not Create Role')
        #test Deletion
        print "Test Delete Role test_roles"  
        role.delete()
        roles = gus_role.objects.filter(_role_name=self.testRole)
        self.assertEqual(len(roles),0,"RoleDeletionError:Unable to Delete Role")
    def test_addUser(self):
	"""
	@summary: test adding users to a role

	@precondition: L{setUp}

	tests L{gus_role.addUser<gus2.gus_roles.models.gus_role.addUser>}
	"""

        gus_role.objects.create_role(self.testGroup, self.testRole)
        role = gus_role.objects.get(_role_name=self.testRole)
	#Test Addition of user role
        print "Test add Role user to role test_roles"  
	role.addUser(self.testUser1)
	self.failUnless(role.users.all()[0] == self.testUser1,'Unable to add user to role')

    def test_getUsers(self):
	"""
	@summary: test getting users
	@precondition: L{setUp}
	tests L{gus_role.getUsers<gus2.gus_roles.models.gus_role.getUser>}
	"""
        gus_role.objects.create_role(self.testGroup, self.testRole)
	role = gus_role.objects.get(_role_name=self.testRole)
	role.addUser(self.testUser1)
	users = role.getUsers()
	print users
	print role.users.all()

    def test_removeUser(self):
	"""
	@summary: test removing users from a role

	@precondition: L{setUp}

	tests L{gus_role.removeUser<gus2.gus_roles.models.gus_role.removeUser>}
	"""
	#Test Deletion of user from role
        print "Test Delete user from Role test_roles"  
        gus_role.objects.create_role(self.testGroup, self.testRole)
	role = gus_role.objects.get(_role_name=self.testRole)
	role.addUser(self.testUser1)
	role.removeUser(self.testUser1)
	userRoles = role.getUsers()
	print userRoles
	self.failUnless(len(userRoles.all()) == 0,"Failed to remove user from role")

