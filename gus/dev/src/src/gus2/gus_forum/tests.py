from django.test import TestCase
from gus2.gus_users.models import gus_user
from gus2.gus_groups.models import gus_group
from models import forum

class ForumTest(TestCase):
	testUser1 = None
	testUser2 = None
	testGroup = None

	def setUp(self):
		testUser1 = gus_user.objects.create_user("a", "b", "p1")
		testUser2 = gus_user.objects.create_user("b", "c", "p2")
		testGroup = gus_group.obects.create_group("name", "test")
	#End


	def TestForumCreateDelete(self):
		"""
		Test creation of a forum
		
		@precondition: L{setUp}
		"""
		
		forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", testGroup)
		grps = forum.objects.filter(forum_name = "TEST FORUM", group = testGroup)
		self.failUnless(len(grps) == 1)
		grps[0].delete()
		grps = forum.objects.filter(forum_name = "TEST FORUM", group = testGroup)
		self.failUnless(len(grps) == 0)
	#End
	
	def TestForumCreateDuplicate(self):
		"""
		Test creation of a forum
		
		@precondition: L{setUp}
		"""
		
		forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", testGroup)
		forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", testGroup)
		grps = forum.objects.filter(forum_name = "TEST FORUM", group = testGroup)
		self.failUnless(len(grps) > 0)
	#End
#End


