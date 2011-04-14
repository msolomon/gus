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
		This will create a new forum tied to a group.
		
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

#	def EditForumDescription(self, Description):
#		"""
#		This allows the forum's description to be changed.
#		
#		@type Description: models.TextField()
#		@param Description: The description to replace the current description.
#		"""
#
#		self.forum_description = Description
#		self.save()
#	#End

	def LastPostDate(self):
		"""
		Returns the date of the last post made in this forum's threads.
		
		@rtype: models.DateTimeField
		@return: The last date a post was made in this forum's threads.
		"""

		last_thread = forum_thread.objects.filter(forum = self).order_by('-date_created')
		if len(last_thread) == 0:
			return 'Never'
		#End
		last_post = forum_post.objects.filter(thread = last_thread[0]).order_by('-date_created')
		if len(last_post) == 0:
			return 'Never'
		#End

		return last_post[0].date_created
	#End

	def LastPostUser(self):
		"""
		Returns the user of the last post made in this forum's threads.
		
		@rtype: gus_roles.models.gus_user
		@return: The user of the last date a post was made in this forum's threads.
		"""

		last_thread = forum_thread.objects.filter(forum = self).order_by('-date_created')
		if len(last_thread) == 0:
			return 'Nobody'
		#End
		last_post = forum_post.objects.filter(thread = last_thread[0]).order_by('-date_created')
		if len(last_post) == 0:
			return 'Nobody'
		#End

		return last_post[0].user
	#End

	def LastPostThread(self):
		"""
		Returns the thread of the last post made in this forum's threads.
		
		@rtype: gus_forum.forum_thread
		@return The thread of the last thread the was posted in this forum's threads.
		"""

		last_thread = forum_thread.objects.filter(forum = self).order_by('-date_created')
		if len(last_thread) == 0:
			return 'None'
		#End

		return last_thread[0]
	#End

	def CreateThread(self, Threadname, User, Text, Forum):
		"""
		Creates a thread for this forum.
		
		@type Threadname: string
		@param Threadname: The name of the thread to be created.
		@type User: gus_user
		@param User: The User to assosciate the thread with.
		@type Text: models.TextField()
		@param Text: The content of the thread.
		@type Forum: forum
		@param Forum: The forum to assosciate the thread with.
		"""

		forum_thread.objects.create(thread_name = Threadname, user = User, thread_text = Text, forum = Forum)
	#End

#	def DeleteThread(self, Thread):
#		"""
#		Allows for the deletion of a thread in this forum as long as the user has admin permissions.
#		
#		@type Thread: forum_thread
#		@param Thread: The thread to be found and deleted.
#		"""
#
#		threads = forum_thread.objects.filter(pk = Thread.id)
#		if(len(threads) > 0):
#			threads[0].delete()
#		#End
#		else:
#			raise Exception("Threads Empty", "List of Threads are Empty.")
#		#End
#	#End
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

	def LastPostDate(self):
		"""
		Returns the date of the last post made in this forum's threads.
		
		@rtype: models.DateTimeField
		@return: The last date a post was made in this forum's threads.
		"""

		last_post = forum_post.objects.filter(thread = self).order_by('-date_created')
		if len(last_post) == 0:
			return 'Never'
		#End

		return last_post[0].date_created
	#End

	def LastPostUser(self):
		"""
		Returns the user of the last post made in this forum's threads.
		
		@rtype: gus_roles.models.gus_user
		@return: The user of the last date a post was made in this forum's threads.
		"""

		last_post = forum_post.objects.filter(thread = self).order_by('-date_created')
		if len(last_post) == 0:
			return 'Nobody'
		#End

		return last_post[0].user
	#End

	def LastPostThread(self):
		"""
		Returns the thread of the last post made in this forum's threads.
		
		@rtype: gus_forum.forum_thread
		@return The thread of the last thread the was posted in this forum's threads.
		"""

		last_thread = forum_thread.objects.filter(forum = self).order_by('-date_created')
		if len(last_thread) == 0:
			return 'None'
		#End

		return last_thread[0]
	#End

	def CreatePost(self, User, Text):
		"""
		Creates a post in this thread.
		
		@type User: gus_user
		@param User: The user the post is to be associated with.
		@type Text: models.TextField()
		@param Text: The content of the post.
		"""

		forum_post.objects.create(user = User, thread = self, post_text = Text)
	#End

#	def DeletePost(self, Post):
#		"""
#		Allows for the deletion of a post in this thread.
#		
#		@type Post: forum_post
#		@param Post: The post to be found and deleted.
#		"""
#
#		posts = forum_post.objects.filter(pk = Post)
#		if(len(posts) > 0):
#			posts[0].delete()
#		#End
#		else:
#			raise Exception("Posts Empty", "The list of posts is empty.")
#		#End
#	#End
#End

class forum_post(models.Model):
	"""
	class forum_post is our model of a forum post.
	"""

	thread = models.ForeignKey(forum_thread)	#The thread this post belongs to.
	user = models.ForeignKey(gus_user)			#The user this post is assosciated with.
	date_created = models.DateTimeField(auto_now_add=True, blank=True)#The date this post was created.
	post_text = models.TextField()				#The content of this post.

#	def EditPost(self, Text):
#		"""
#		This allows the post's text to be changed.
#		
#		@type Text: models.TextField()
#		@param Text: The text to replace the current text.
#		"""
#
#		self.post_text = Text
#		self.save()
#    #End
#End
