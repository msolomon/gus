from django.db import models
from django import template
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User,Group,Permission,UserManager
from backends import *

register = template.Library()
#extending django's user lets us use all the perks of well ... django users :)
def get_user_by_fullname(uname):
	name=uname.split()
	fname = name[0]
	try:
		lname = name[1] 
	except IndexError:
		lname= ""
	return gus_user.objects.filter(first_name=fname,last_name=lname)
	
class gus_user(User):
	_token=models.CharField(max_length=50)
	def user(self):
		return self
	def get_group_role(self,group):	1
		#let backend handle actual permission fetches ... since we just override the backend
 	def get_all_permissions(self,group):
		be=gus_custom_backend()
		return be.get_grouprole_permissions(self,group)
	def has_perm(self,group,perm):
		be=gus_custom_backend()
		return be.has_perm(self,group,perm)
	def __unicode__(self):
		return self.get_full_name()
	objects = UserManager() #get the usermanager functions


#django's built in groups are more like our roles in that they limit the "permissions" a user has
#so we will build our group from scratch.
class gus_group(models.Model):
	group_name=models.CharField(unique=True,max_length=100) #a string... must be unique...
	is_public = models.BooleanField(blank=True)  #open recruitement
	parent	=   models.ForeignKey('self',null=True,blank=True)  #self aggregation
	def save(self):
		super(gus_group,self).save() #call real save
		#when we save we want to create 2 new roles (only if we have no roles)
		if(len(gus_roles.objects.filter(gid=self))==0):
			r=gus_roles(role_name='Owner',gid=self)
			r.save()
			r=gus_roles(role_name='Admin',gid=self)
			r.save();
			r=gus_roles(role_name='Member',gid=self);
			r.save()

	def get_user_role(self,user):1
#		return usergrouprole(user,self)
	def get_users(self):
		return "users comming soon"

	def __unicode__(self):
		return self.group_name
	
# by extending django's built in group class we have access to all its cool stuff
class gus_roles(Group):
	gid=models.ForeignKey(gus_group)	
	role_name=models.CharField(max_length=100)
	users = models.ManyToManyField(gus_user)
	perms = models.ManyToManyField(Permission)
	def save(self):
		self.name=self.gid.group_name+"."+self.role_name	
		super(gus_roles,self).save() #call real save
	def __unicode__(self):
		return self.name

class user_token(models.Model):
	_user=models.ForeignKey(gus_user)
	_token=models.CharField(max_length=50)
	_username=models.CharField(max_length=50)
	def is_validated(self):
		if self._user > -1 :
			u = gus_user.objects.get(pk=self._user).get(_token=self._token)
			if(u):
				return "asd"
			else :
				return "xyz"


def usergrouprole(user,group):
	try:
		return gus_roles.objects.filter(gid=group,uid=user)[0]
	except IndexError:
		return None

def authenticate(username,password):
        try:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
                return None
        if user.check_password(password):return user
        return None

def setup_and_save_tokens(request,user):
        try:
                u2=gus_user.objects.get(_user=user)
        except gus_user.DoesNotExist:
                return None
        u2._token =generate_token(user)
        u2.save()
        try:
                CToken = user_token.objects.get(_user=u2)
        except user_token.DoesNotExist:
                CToken = user_token()
                CToken._user=u2
        CToken._token=u2._token
        CToken._username = user.username
        CToken.save()
        request.session['user'] = CToken._token
        request.session.save()

def userauthenticated(request):
	try:
	        key = request.session['user']
	except KeyError:
		return
	try:
	        u=gus_user.objects.get(_token=key)
	except gus_user.DoesNotExist:
		return
        return u


def generate_token(user):
        import time
        from datetime import datetime
        import hashlib
        base=str(datetime.now())+user.password+user.username
        return  hashlib.sha1(base).hexdigest();


