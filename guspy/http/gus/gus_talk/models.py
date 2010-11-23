from gus.gus_groups.models import *
from django.db import models
# Create your models here.

class gus_message(models.Model):
	_text=models.TextField()
	_author=models.ForeignKey(gus_user,related_name="author")
	_timestamp=models.DateField(auto_now_add=True)
	_recipient=models.ForeignKey(gus_user,null=True,blank=True,related_name="recipient")

class gus_thread(models.Model):
	_title=models.CharField(max_length=100)
	_messages=models.ManyToManyField(gus_message)
	_created=models.DateField(auto_now_add=True)
	_updated=models.DateField(auto_now_add=True)

class gus_forum(models.Model):
	_title=models.CharField(max_length=100)
	_threads=models.ManyToManyField(gus_thread,blank=True)
	_access=models.ManyToManyField(gus_roles,blank=True)
