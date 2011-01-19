from django.db import models
from gus_forum.models import forum

class forum_thread():
	"""
	class forum_thread is our model of a thread.
	?
	"""
	
	thread_id = models.IntegerField() #Thread's ID
	forum_id = models.IntegerField() #Forum ID this thread belongs to.
	user_id = models.IntegerField() #ID of user who created this thread.
	date_created = models.DateTimeField() #Thread creation date.
	thread_name = models.CharField(max_length=25) #Thread's name.
	thread_posts #Some list like thing holding the thread's posts... ???
	
	def CreatePost(self,user_id,text):
		"""
		Creates a post in this thread as long as the user has the proper permissions.
		?
		"""
	
		#Create post, set it's user_id & text... 
		raise Exception("In Dev", "This Is Unfinished")
	#End
	
	def DeletePost(self,post_id):
		"""
		Allows for the deletion of a post in this thread as long s the user has admin permissions.
		?
		"""
		
		#Find post, nuke it...
		raise Exception("In Dev", "This Is Unfinished")
	#End
	