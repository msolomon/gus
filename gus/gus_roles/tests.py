"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from gus.gus_groups.models import gus_group
from gus.gus_roles.models import gus_role
from gus.gus_users.models import gus_user

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
        @requires: L{gus_group.create_group<gus.gus_groups.models.GroupManager.create_group>}
        @requires: L{gus_user.create_user<gus.gus_users.models.UserManager.create_user>}
        """
        self.testGroup = gus_group.objects.create_group("TestGroup1", "Added For Testing Roles", '')
        self.testUser1  = gus_user.objects.create_user("Test User1", "test@user1", '1')
        self.testUser2  = gus_user.objects.create_user("Test User2", "test@user2", '2')
        
    def test_createAndDelete_role(self):
        """
    	@summary:  tests that roles can be created
    	
    	@precondition: L{setUp}
    	
    	tests built in django model deletion
    	and L{gus_role.create_role<gus.gus_roles.models.RoleManager.create_role>} 
    	"""
        group_object = gus_group.objects.create_group(self.testRole, 'test', '')
        #Test Creation
        role = gus_role.objects.create_role(group_object, self.testRole)
        self.failUnlessEqual(role._role_name, self.testRole,'RoleCreationError:Could Not Create Role')
        #test Deletion
        role.delete()
        roles = gus_role.objects.filter(_role_name=self.testRole)
        self.assertEqual(len(roles),0,"RoleDeletionError:Unable to Delete Role")
    def test_addUser(self):
	"""
	@summary: test adding users to a role

	@precondition: L{setUp}

	tests L{gus_role.addUser<gus.gus_roles.models.gus_role.addUser>}
	"""

        role = gus_role.objects.create_role(self.testGroup, self.testRole)
	#Test Addition of user role
	role.addUser(self.testUser1)
	self.failUnless(role.users.all()[0] == self.testUser1,'Unable to add user to role')

    def test_getUsers(self):
	"""
	@summary: test getting users
	@precondition: L{setUp}
	tests L{gus_role.getUsers<gus.gus_roles.models.gus_role.getUser>}
	"""
        role = gus_role.objects.create_role(self.testGroup, self.testRole)
	role.addUser(self.testUser1)
	users = role.getUsers()
	self.failUnless(len(users.all()) != 0,'Failed to get users')

    def test_getGroup(self):
	"""
	@summary: test getting groups
	@precondition: L{setUp}
	tests L{gus_role.getGroup<gus.gus_roles.models.gus_role.getGroup>}
	"""
        role = gus_role.objects.create_role(self.testGroup, self.testRole)
	test_group = role.getGroup()
	self.failUnlessEqual(test_group,self.testGroup,'Failed to get group')

    def test_removeUser(self):
	"""
	@summary: test removing users from a role

	@precondition: L{setUp}

	tests L{gus_role.removeUser<gus.gus_roles.models.gus_role.removeUser>}
	"""
	#Test Deletion of user from role
        role = gus_role.objects.create_role(self.testGroup, self.testRole)
	role.addUser(self.testUser1)
	role.removeUser(self.testUser1)
	userRoles = role.getUsers()
	self.failUnless(len(userRoles.all()) == 0,"Failed to remove user from role")

    def test_permString(self):
	"""
	@summary: test application of permissions
	@precondition: L{setUp}
	tests L{gus_role.with_user_in_group<gus.gus_roles.models.gus_role.permString>}
	"""
	from django.contrib.auth.models import Permission
	role = gus_role.objects.create_role(self.testGroup, self.testRole)
	role._role_permissions.permissions.add(Permission.objects.all()[0])
	self.failUnless(len(role.permString()) != 0, "Failed to get permisions for role/group")

    def test_with_user_in_group(self):
	"""
	@summary: test getting a role by a user and a group
	@precondition: L{setUp}
	tests L{gus_role.with_user_in_group<gus.gus_roles.models.gus_role.with_users_in_group>}
	"""
        role = gus_role.objects.create_role(self.testGroup, self.testRole)
	role.addUser(self.testUser1)
	test_role = gus_role.objects.with_user_in_group(self.testGroup,self.testUser1)
	self.failUnlessEqual(test_role[0]._role_name, self.testRole,'Failed to get role of user in group')	

    def test_with_user(self):
	"""
	@summary: tests the with_user function
	@precondition: L{setUp}
	tests L{gus_role.with_user<gus.gus_roles.models.gus_role.with_users>}
	"""
        role = gus_role.objects.create_role(self.testGroup, self.testRole)
	role.addUser(self.testUser1)
	test_role = gus_role.objects.with_user(self.testUser1)
	self.failUnlessEqual(test_role[0]._role_name, self.testRole,'Failed to get roles for user')
	
    def test_with_group(self):
	"""
	@summary: test the with_group function
	@precondition: L{setUp}
	tests L{gus_role.with_group<gus.gus_roles.models.gus_role.with_group>}
	"""
        role = gus_role.objects.create_role(self.testGroup, self.testRole)
	test_role = gus_role.objects.with_group(self.testGroup)
	self.failUnlessEqual(test_role[0]._role_name, self.testRole,'Failed to get roles of given group')
	
    def test_unicode(self):
	"""
        @summary: test the __unicode__ function
	@precondition: L{setUp}
        tests L{gus_role.with_group<gus.gus_roles.models.gus_role.with_group>}
        """
        role = gus_role.objects.create_role(self.testGroup, self.testRole)
	self.failUnlessEqual(role.__unicode__(),'Role :[TestGroup1] testRole',"unexpected unicode response")
