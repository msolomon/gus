from django.db import models
from django.contrib.auth.models import User,Group,Permission

class gus_user(models.Model):
	_user=models.OneToOneField(User)
	def __unicode__(self):
		return self._user.username

class gus_group(models.Model):
	_group=models.OneToOneField(Group)
	def __unicode__(self):
		return self._group.name
	
class gus_roles(models.Model):
	gid=models.ForeignKey(gus_group)
	uid=models.ManyToManyField(gus_user)
	permissions=models.ManyToManyField(Permission)
	role_name=models.CharField(max_length=100)

