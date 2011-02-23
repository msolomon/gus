from django.test import TestCase
from gus.gus_users.models import gus_user
from gus.gus_groups.models import gus_group
from gus.gus_forum.models import *

class ForumTest(TestCase):
	testUser1 = None
	testUser2 = None
	testGroup = None

	def setUp(self):
		"""
		Sets up two test users and one test group.
		"""
		
		self.testUser1 = gus_user.objects.create_user("a", "b", "p1")
		self.testUser2 = gus_user.objects.create_user("b", "c", "p2")
		self.testGroup = gus_group.objects.create_group("name", "test", "test2")
	#End


	def test_ForumCreateDelete(self):
		"""
		Tests the creation of a forum.
		
		@precondition: L{setUp}
		"""
		
		forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", self.testGroup)
		grps = forum.objects.filter(forum_name = "TEST FORUM", group = self.testGroup)
		self.failUnless(len(grps) == 1)
		grps[0].delete()
		grps = forum.objects.filter(forum_name = "TEST FORUM", group = self.testGroup)
		self.failUnless(len(grps) == 0)
	#End
	
	def test_ForumCreateDuplicate(self):
		"""
		Tests the creation of duplicate forums.
		
		@precondition: L{setUp}
		"""
		
		forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", self.testGroup)
		try:
			forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", self.testGroup)
		except:
			pass
		grps = forum.objects.filter(forum_name = "TEST FORUM", group = self.testGroup)
		self.failUnless(len(grps) > 0)
	#End
	
	def test_ForumCreateEditDescription(self):
		"""
		Tests the creation of a forum & changing the forum's name & description.
		
		@precondition: L{setUp}
		"""
		
		forum.objects.create_forum("TESTFORUM", "THIS IS A TEST FORUM DESCRIPTION", self.testGroup)
		frm = forum.objects.filter(forum_name = "TESTFORUM", group = self.testGroup)
		self.failUnless(len(frm) > 0)
		frm[0].EditForumDescription("TEST FORUM'S NEW DESCRIPTION")
		frm = forum.objects.filter(forum_description = "TEST FORUM'S NEW DESCRIPTION", group = self.testGroup)
		self.failUnless(len(frm) > 0)
	#End
	
	def test_ForumCreateThread(self):
		"""
		Test the creation of creation of threads.
		
		@precondition: L{setUp}
		"""
		
		forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", self.testGroup)
		frm = forum.objects.filter(forum_name = "TEST FORUM", group = self.testGroup)
		self.failUnless(len(frm) > 0)
		frm[0].CreateThread("TESTTHREAD", self.testUser1, "This is a test thread.", frm[0])
		thd = forum_thread.objects.filter(thread_name = "TESTTHREAD", user = self.testUser1)
		self.failUnless(len(thd) > 0)
	#End
	
	def test_ForumDeleteThread(self):
		"""
		Tests the deletion of threads.
		
		@precondition: L{setUp}
		"""
		
		forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", self.testGroup)
		frm = forum.objects.filter(forum_name = "TEST FORUM", group = self.testGroup)
		self.failUnless(len(frm) > 0)
		frm[0].CreateThread("TESTTHREAD", self.testUser1, "This is a test thread.", frm[0])
		thd = forum_thread.objects.filter(thread_name = "TESTTHREAD", user = self.testUser1)
		self.failUnless(len(thd) > 0)
		frm[0].DeleteThread(thd[0])
		thd = forum_thread.objects.filter(thread_name = "TESTTHREAD", user = self.testUser1)
		self.failUnless(len(thd) == 0)
	#End
	
	def test_ForumCreatePost(self):
		"""
		Tests the creation of posts.
		
		@precondition: L{setUp}
		"""
		
		forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", self.testGroup)
		frm = forum.objects.filter(forum_name = "TEST FORUM", group = self.testGroup)
		self.failUnless(len(frm) > 0)
		frm[0].CreateThread("TESTTHREAD", self.testUser1, "This is a test thread.", frm[0])
		thd = forum_thread.objects.filter(thread_name = "TESTTHREAD", user = self.testUser1)
		self.failUnless(len(thd) > 0)
		thd[0].CreatePost(self.testUser1, "THIS IS A TEST POST")
		pst = forum_post.objects.filter(post_text = "THIS IS A TEST POST", user = self.testUser1)
		self.failUnless(len(thd) > 0)
	#End
	
	def test_ForumDeletePost(self):
		"""
		Tests the deletion of posts.
		
		@precondition: L{setUp}
		"""
		
		forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", self.testGroup)
		frm = forum.objects.filter(forum_name = "TEST FORUM", group = self.testGroup)
		self.failUnless(len(frm) > 0)
		frm[0].CreateThread("TESTTHREAD", self.testUser1, "This is a test thread.", frm[0])
		thd = forum_thread.objects.filter(thread_name = "TESTTHREAD", user = self.testUser1)
		self.failUnless(len(thd) > 0)
		thd[0].CreatePost(self.testUser1, "THIS IS A TEST POST")
		pst = forum_post.objects.filter(post_text = "THIS IS A TEST POST", user = self.testUser1)
		self.failUnless(len(pst) > 0)
		thd[0].DeletePost(pst)
		pst = forum_post.objects.filter(post_text = "THIS IS A TEST POST", user = self.testUser1)
		self.failUnless(len(pst) == 0)
	#End
	
	def test_ForumEditPost(self):
		"""
		Tests editing of exisiting posts.
		
		@precondition: L{setUp}
		"""
		
		forum.objects.create_forum("TEST FORUM", "THIS IS A TEST FORUM DESCRIPTION", self.testGroup)
		frm = forum.objects.filter(forum_name = "TEST FORUM", group = self.testGroup)
		self.failUnless(len(frm) > 0)
		frm[0].CreateThread("TESTTHREAD", self.testUser1, "This is a test thread.", frm[0])
		thd = forum_thread.objects.filter(thread_name = "TESTTHREAD", user = self.testUser1)
		self.failUnless(len(thd) > 0)
		thd[0].CreatePost(self.testUser1, "THIS IS A TEST POST")
		pst = forum_post.objects.filter(post_text = "THIS IS A TEST POST", user = self.testUser1)
		self.failUnless(len(pst) > 0)
		pst[0].EditPost("THIS IS AN EDITED TEST POST")
		pst = forum_post.objects.filter(post_text = "THIS IS AN EDITED TEST POST", user = self.testUser1)
		self.failUnless(len(pst) > 0)
	#End
#End


