from django.db import models
from gus.gus_widget.models import Widget
from gus.gus_users.models import gus_user
from gus.gus_groups.models import gus_group

class ForumManager(models.Manager):
	"""
	class ForumManager manages the creation of forums.
	"""

	def create_forum(self, Name, Description, Group):
		"""
		This will create a new forum.
		
		@type Name: models.CharField()
		@param Name: The name of the forum being created.
		@type Description: models.TextField()
		@param Description: The description of the forum being created.
		@type Group: gus_group
		@param Group: The group this forum is associated with.
		@rtype: 
		@return: The newly created forum.
		"""

		forums = forum.objects.filter(forum_name = Name, group = Group)
		if(len(forums) > 0):
			raise Exception("Forum Exists", "There already exists a forum named %s" %Name)
		#End
		return super(ForumManager, self).get_query_set().create(forum_name = Name, forum_description = Description, group = Group)
	#End
#End
			
class forum(models.Model):
	"""
	class forum is our model of a forum.
	"""

	objects = ForumManager()					#
	group = models.ForeignKey(gus_group)		#The Group the forum belongs to.
	forum_name = models.CharField(max_length=25)#The forum's name.
	forum_description = models.TextField()		#The forum's description.

	def __unicode__(self):
		return "%s: %s\n%s"%(self.forum_name, self.forum_description, self.group)

	def EditForumDescription(self, Description):
		"""
		This allows the forum's description to be changed as long as the user has the proper permissions.
		
		@type Description: models.TextField()
		@param Description: The description to replace the current description.
		"""

		if 1: #valid_userpermissions()
			self.forum_description = Description
			self.save()
		#End
		else:
			raise Exception("Invalid Permissions", "User does not have permission to do this.")
		#End
	#End

	def CreateThread(self, Threadname, User, Text, Forum):
		"""
		Creates a thread for this forum as long as the user has the proper permissions.
		
		@type Threadname: string
		@param Threadname: The name of the thread to be created.
		@type User: gus_user
		@param User: The User to assosciate the thread with.
		@type Text: models.TextField()
		@param Text: The content of the thread.
		@type Forum: forum
		@param Forum: The forum to assosciate the thread with.
		"""

		if 1: #valid_userpermissions()
			forum_thread.objects.create(thread_name = Threadname, user = User, thread_text = Text, forum = Forum)
		#End
		else:
			raise Exception("Invalid Permissions", "User does not have permission to do this.")
		#End
	#End

	def DeleteThread(self, Thread):
		"""
		Allows for the deletion of a thread in this forum as long as the user has admin permissions.
		
		@type Thread: forum_thread
		@param Thread: The thread to be found and deleted.
		"""

		if 1: #valid_userpermissions()
			threads = forum_thread.objects.filter(pk = Thread.id)
			if(len(threads) > 0):
				threads[0].delete()
			#End
			else:
				raise Exception("Threads Empty", "List of Threads are Empty.")
			#End
		#End
		else:
			raise Exception("Invalid Permissions", "User does not have permission to do this.")
		#End
	#End
#End

class forum_thread(models.Model):
	"""
	class forum_thread is our model of a forum thread.
	"""

	forum = models.ForeignKey(forum)				#The forum this thread belongs to.
	user = models.ForeignKey(gus_user)				#The user who created this thread.
	date_created = models.DateTimeField(auto_now_add=True, blank=True)#The thread's creation date.
	thread_name = models.CharField(max_length=25)	#The thread's name.
	thread_text = models.TextField()				#The thread's content.

	def __unicode__(self):
		return "%s - %s: %s\n%s\nFrom Forum: %s"%(self.date_created, self.thread_name, self.thread_text, self.user, self.forum)

	def CreatePost(self, User, Text):
		"""
		Creates a post in this thread as long as the user has the proper permissions.
		
		@type User: gus_user
		@param User: The user the post is to be associated with.
		@type Text: models.TextField()
		@param Text: The content of the post.
		"""

		if 1: #valid_userpermissions()
			forum_post.objects.create(user = User, thread = self, post_text = Text)
		#End
		else:
			raise Exception("Invalid Permissions", "User does not have permission to do this.")
		#End
	#End

	def DeletePost(self, Post):
		"""
		Allows for the deletion of a post in this thread as long as the user has admin permissions.
		
		@type Post: forum_post
		@param Post: The post to be found and deleted.
		"""

		if 1: #valid_userpermissions()
			posts = forum_post.objects.filter(pk = Post)
			if(len(posts) > 0):
				posts[0].delete()
			#End
			else:
				raise Exception("Posts Empty", "The list of posts is empty.")
			#End
		#End
		else:
			raise Exception("Invalid Permissions", "User does not have permission to do this.")
		#End
	#End
#End

class forum_post(models.Model):
	"""
	class forum_post is our model of a forum post.
	"""

	thread = models.ForeignKey(forum_thread)	#The thread this post belongs to.
	user = models.ForeignKey(gus_user)			#The user this post is assosciated with.
	date_created = models.DateTimeField(auto_now_add=True, blank=True)#The date this post was created.
	post_text = models.TextField()				#The content of this post.

	def __unicode__(self):
		return "On %s by %s\n%s\nFrom Thread: %s"%(self.date_created, self.user, self.post_text, self.thread)

	def EditPost(self, Text):
		"""
		This allows the post's text to be changed as long as the user has the proper permissions.
		
		@type Text: models.TextField()
		@param Text: The text to replace the current text.
		"""

		if 1: #valid_userpermissions()
			self.post_text = Text
			self.save()
		#End
		else:
			raise Exception("Wrong Permissions", "User does not have permission to do this.")
		#End
    #End
#End
