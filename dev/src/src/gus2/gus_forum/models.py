from django.db import models
from gus_widget.models import Widget

class forum_post(forum_thread):
    """
    class forum_post is our model of a forum post.
    """
    
    thread_id = models.ForeignKey(forum_thread)
    post_id = models.IntegerField() 
    user_id = models.ForeignKey(user)
    date_created = models.DateTimeField()
    
    #Post text; not sure if we need a max post length. This is the only field that can be modified within this class
    post_content = models.CharField(max_length=5000)
    
    def EditPost(self,user_id):
        """
        Allows a user to edit the text of a post if they have the proper user_id, giving direct access to post_content
        """
		
		#if #valid user permissions
			raise Exception("In development", "This function does not work yet")
		#End
		#else
		#	raise Exception("In development", "This function does not work yet")
		#End
    #End
#End

class forum_thread(forum):
	"""
	class forum_thread is our model of a forum thread.
	?
	"""
	
	thread_id = models.IntegerField() #Thread's ID
	forum_id = models.ForeignKey(forum) #Forum ID this thread belongs to.
	user_id = models.ForeignKey(user) #ID of user who created this thread.
	date_created = models.DateTimeField() #Thread creation date.
	thread_name = models.CharField(max_length=25) #Thread's name.
	thread_posts = models.OneToManyField() #A list of forum_posts
	
	def CreatePost(self,user_id,text):
		"""
		Creates a post in this thread as long as the user has the proper permissions.
		?
		"""
	
		#if #valid user permissions
			#Create post, set it's user_id & text...
		#	raise Exception("In Dev", "This Is Unfinished")
		#End
		#else
			raise Exception("Wrong Permissions", "User does not have permission to do this.")
		#End
	#End
	
	def DeletePost(self,post_id):
		"""
		Allows for the deletion of a post in this thread as long s the user has admin permissions.
		?
		"""
		
		#if #valid user permissions
			#Find post, nuke it...
		#	raise Exception("In Dev", "This Is Unfinished")
		#End
		#else
			raise Exception("In Dev", "This Is Unfinished")
		#End
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
	forum_threads = models.ManyToOneField() #A list of forum_threads
	
	def EditForumDescription(self,description):
		"""
		This allows the forum's description to be changed as long as the user has the proper permissions.
		?
		"""
		
		#if #valid user permissions
		#	self.forum_description = description
		#End
		#else
			raise Exception("Wrong Permissions", "User does not have permission to do this.")
		#End
	#End
	
	def CreateThread(self,thread_name,user_id):
		"""
		Creates a thread for this forum as long as the user has the proper permissions.
		?
		"""
		
		#if #valid user permissions
			#Create the thread, set it's stuff, add it to forum's thread list...
		#	forum_thread temp()
		#	raise Exception("In Dev", "This Is Unfinished")
		#End
		#else
			raise Exception("In Dev", "This Is Unfinished")
		#End
	#End
	
	def DeleteThread(self,thread_id):
		"""
		Allows for the deletion of a thread in this forum as long as the user has admin permissions.
		?
		"""
	
		#if #valid user permissions
			#Find thread, nuke it...
		#	raise Exception("In Dev", "This Is Unfinished")
		#End
		#else
			raise Exception("In Dev", "This Is Unfinished")
		#End
	#End
#End
