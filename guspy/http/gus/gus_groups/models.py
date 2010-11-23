from django.db import models
from django.contrib.auth.models import User,Group,Permission



class gus_user(models.Model):
	_user=models.OneToOneField(User)

	def __unicode__(self):
		return self._user.username

class gus_group(models.Model):
	group_name=models.CharField(unique=True,max_length=100)
	is_public = models.BooleanField(blank=True)

	def save(self):
		super(gus_group,self).save() #call real save
		r=gus_roles(role_name='Admin',gid=self)
		r.save();
		r=gus_roles(role_name='Member',gid=self);
		r.save()

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
