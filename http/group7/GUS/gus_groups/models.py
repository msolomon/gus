from django.db import models
from django.contrib.auth.models import User,Group
from django.template.loader import render_to_string


############################USER CLASS#################################
class gus_user(models.Model):
"""
	Use: u = gus_user(<userObject>) \n
	This just extends the Usermodel slightly and will serve as a key"""
"""
	def __init__(self,usr):
	"""
		expects an argument of type User(django.auth)
	"""
		self.pid=usr.id

	real_name=models.CharField(max_length=200)
	pid=models.ForeignKey(User)


######################GROUP CLASS#####################################
class gus_group(models.Model):
"""
	Use:g = gus_group(<groupObject>)\n
	likewise just extents the group object for our needs
"""
	###METHODS
	def __init__(self,grp):
	"""
		expects an argument of type Group(django.auth)
	"""
		self.pid=grp.id
	###DATA MEMBERS
	description=models.CharField(max_length=200)
	pid=models.ForeignKey(Group)

#######################################################
class associator(models.Model):
"""
	use: associator(<gus_user>,<gus_group>)
"""
	###METHODS
		#None
	###DATA MEMBERS
	pid=models.ForeignKey(gus_user)
	pid=models.ForeignKey(gus_group)


#######################Helper Class should probably just be a helper....
class display_user(models.Model):
	""" Use: disp=display_user(<user_object>,<func_name>)\n
		 print(<user_object>) #print the user in specified mode
	this class is just something to assist printing of users"""
	user=None
	def __init__(self,user,display_type):
		S="self."+display_type+"()"
		eval( S)
	def show_all(self):
		""" Use: disp.show_all()\n
		Sets User Display to VERY verbose
		"""
#		self.user.__unicode__=self.all_data_str()
	

	def all_data_str(self):
		"""Use: disp.all_data_str()\n
		Returns a HTML FORMATTED TEMPLATE"""
		rendered = render_to_string('gus_groups/show_user.html',
					 { 'user': self.user })
		print rendered
