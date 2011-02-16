from django.db import models
from gus.gus_widget.models import Widget
from gus.gus_users.models import gus_user
from gus.gus_groups.models import gus_group

class ForumManage(models.Manager):
	"""
	class ForumManage manages forums.
	?
	"""

	def create_forum(self, name, description, groupid):
        #"""
        #this will create a new user and insert it into the table
		#?
		#"""

		grps = forum.objects.filter(forum_name = name, group_id = groupid)
		if(len(grps) > 0):
			raise Exception("Forum Exists", "There already exists a forum named %s" %name)
		#End
		return super(ForumManager, self).get_query_set().create(forum_name = name, forum_description = description, group = groupid)
	#End
#End
			
class forum(Widget):
	"""
	class forum is our model of a forum.
	?
	"""

	forum_id = models.IntegerField() #The forum's ID.
	group_id = models.ForeignKey(gus_group) #The group's ID the forum belongs to.
	forum_name = models.CharField(max_length=25) #The forum's name. 
	forum_description = models.TextField() #The forum's description.
	#forum_threads = models.OneToManyField(forum_thread) #A list of forum_threads

	def EditForumDescription(self, description):
		"""
		This allows the forum's description to be changed as long as the user has the proper permissions.
		?
		"""

		if 1: #valid_userpermissions()
			self.forum_description = description
			self.save()
		#End
		else:
			raise Exception("Wrong Permissions", "User does not have permission to do this.")
		#End
	#End

	def CreateThread(self, threadname, userid, intext, forumid):
		"""
		Creates a thread for this forum as long as the user has the proper permissions.
		?
		"""

		if 1: #valid_userpermissions()
			forum_thread.objects.create(thread_name = threadname, user = userid, text = intext, forum = fourmid)
		#End
		else:
			raise Exception("Wrong Permissions", "User does not have permission to do this.")
		#End
	#End

	def DeleteThread(self, threadid):
		"""
		Allows for the deletion of a thread in this forum as long as the user has admin permissions.
		?
		"""

		if 1: #valid_userpermissions()
			threads = forum_thread.objects.filter(pk = threadid)
			if(len(threads) > 0):
				threads[0].delete()
			#End
			else:
				raise Exception("Threads Empty", "List of Threads are Empty.")
			#End
		#End
		else:
			raise Exception("Wrong Permissions", "User does not have permission to do this.")
		#End
	#End
#End

class forum_post(models.Model):
    """
    class forum_post is our model of a forum post.
    """

    #thread = models.ForeignKey(forum_thread)
    post = models.IntegerField() 
    user = models.ForeignKey(gus_user)
    date_created = models.DateTimeField(auto_now_add = True)
    post_content = models.TextField()

    def EditPost(self, text):
		"""
		Allows a user to edit the text of a post if they have the proper user_id, giving direct access to post_content
		"""

		if 1: #valid_userpermissions()
			self.post_content = text
			self.save()
		#End
		else:
			raise Exception("Wrong Permissions", "User does not have permission to do this.")
		#End
    #End
#End

class forum_thread(models.Model):
	"""
	class forum_thread is our model of a forum thread.
	?
	"""

	forum = models.ForeignKey(forum) #Forum ID this thread belongs to.
	user = models.ForeignKey(gus_user) #ID of user who created this thread.
	date_created = models.DateTimeField() #Thread creation date.
	thread_name = models.CharField(max_length=25) #Thread's name.
	text = models.TextField()
	#thread_posts = models.OneToManyField(forum_post) #A list of forum_posts

	def CreatePost(self, userid, text):
		"""
		Creates a post in this thread as long as the user has the proper permissions.
		?
		"""

		if 1: #valid_userpermissions()
			forum_post.objects.create(user = userid, thread = this, post_content = text)
		#End
		else:
			raise Exception("Wrong Permissions", "User does not have permission to do this.")
		#End
	#End

	def DeletePost(self, postid):
		"""
		Allows for the deletion of a post in this thread as long as the user has admin permissions.
		?
		"""

		if 1: #valid user permissions
			posts = forum_post.objects.filter(pk = postid)
			if(len(posts) > 0):
				posts[0].delete()
			#End
			else:
				raise Exception("Posts Empty", "List of Post are Empty.")
			#End
		#End
		else:
			raise Exception("Wrong Permissions", "User does not have permission to do this.")
		#End
	#End
#End
