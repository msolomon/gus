from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.


class gus_user(models.Model):
	user_handle = models.CharField(max_length=100)
	pid	    = models.ForeignKey(User)

class gus_group(models.Model):
	group_owner= models.ForeignKey(gus_user)
	group_name = models.CharField(max_length=100)
	group_desc = models.CharField(max_length=300)
	pid	   = models.ForeignKey(Group)

class gus_roles(models.Model):
	gid=models.ForeignKey(gus_group)
	users = models.ManyToManyField(gus_user)
	status_word=models.IntegerField()
	role_name=models.CharField(max_length=100)
	role_desc=models.CharField(max_length=255)


class gus_contact_info(models.Model):
	myuser = models.ForeignKey(gus_user)
	real_name=models.CharField(max_length=100)
	phone_number=models.CharField(max_length=11)
	email=models.CharField(max_length=200)
	address1=models.CharField(max_length=100)
	address2=models.CharField(max_length=100)


