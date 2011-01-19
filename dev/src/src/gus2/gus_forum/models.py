from django.db import models
from gus_widget.models import Widget

class forum(Widget):
	"""
	class forum is our model of a forum.
	?
	"""
	
	forum_id = models.IntegerField() #The forum's ID.
	group_id = models.IntegerField() #The group's ID the forum belongs to.
	forum_name = models.CharField(max_length=25) #The forum's name. 
	forum_descrip = models.TextField() #The forum's description.
	forum_threads #Some list like thing holding the forum's threads... ???
	
	def EditForum(self,text):
		"""
		This allows the forum's description to be changed as long as the user has the the proper permissions.
		?
		"""
		
		self.forum_descrip = text
		raise Exception("In Dev", "This Is Unfinished")
	#End
	
	def CreateThread(self,thread_name,user_id):
		"""
		Creates a thread for this forum as long as the user has the proper permissions.
		?
		"""
		
		#Create the thread, set it's stuff, add it to forum's thread list...
		raise Exception("In Dev", "This Is Unfinished")
	#End
	
	def DeleteThread(self,thread_id):
		"""
		Allows for the deletion of a thread in this forum as long as the user has admin permissions.
		?
		"""
	
		#Find thread, nuke it...
		raise Exception("In Dev", "This Is Unfinished")
	#End
#End
