from django.db import models
from django import template
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User,Group,Permission
from backends import *

register = template.Library()

class gus_user(models.Model):
	_user=models.OneToOneField(User)
	_token=models.CharField(max_length=50)
	def user(self):
		return self._user

	def get_group_role(self,group):
		return usergrouprole(self,group)
	
	def get_all_permissions(self,group):
		be=gus_custom_backend()
		return be.get_grouprole_permissions(self,group)
	def has_perm(self,group,perm):
		be=gus_custom_backend()
		return be.has_perm(self,group,perm)
	def __unicode__(self):
		return self._user.username

class gus_group(models.Model):
	group_name=models.CharField(unique=True,max_length=100) #a string... must be unique...
	is_public = models.BooleanField(blank=True)  #open recruitement
	parent	=   models.ForeignKey(gus_group)  #self aggregation
	def save(self):
		super(gus_group,self).save() #call real save
		r=gus_roles(role_name='Admin',gid=self)
		r.save();
		r=gus_roles(role_name='Member',gid=self);
		r.save()
	def get_user_role(self,user):
		return usergrouprole(user,self)
	def get_users(self):
		return "users comming soon"

	def __unicode__(self):
		return self.group_name
	
class gus_roles(models.Model):
	gid=models.ForeignKey(gus_group)
	uid=models.ManyToManyField(gus_user,blank=True,null=True)
	permissions=models.ManyToManyField(Permission)
	role_name=models.CharField(max_length=100)
	def save(self):
		super(gus_roles,self).save() #call real save
	def __unicode__(self):
		if(self.id):return self.role_name+"  ("+str(self.uid.count())+")"
		return ""

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


