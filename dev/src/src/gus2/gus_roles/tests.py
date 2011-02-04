"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from gus2.gus_groups.models import gus_group
from gus2.gus_roles.models import gus_role

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

    def test_create_role(self):
	"""
	tests that roles can be created
	"""
	print "Test Create Role test_roles"  
	group_object = gus_group.objects.create_group('test_roles','test','')
	gus_role.objects.create_role(group_object,'test_role')
	role = gus_role.objects.get(_role_name='test_role')
	self.failUnlessEqual(role._role_name, 'test_role')
	print "Test successful"

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

