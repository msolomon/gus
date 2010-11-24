from gus.gus_groups.models import *
from django import forms
from django.db import models
# Create your models here.


class gus_forum(models.Model):
	_title = models.CharField(max_length=50)
	_group = models.ForeignKey(gus_group)
	def __unicode__(self):
		return self._title

class gus_thread(models.Model):
	_forum = models.ForeignKey(gus_forum)
	_title = models.CharField(max_length=50)
	created = models.DateTimeField(auto_now_add=True)
    	creator = models.ForeignKey(User, blank=True, null=True)
	def __unicode__(self):
		return unicode(self.creator)+" - "+self._title

class gus_message(models.Model):
	_title  = models.CharField(max_length=50)
	_body   = models.TextField(max_length=10000)
	_thread = models.ForeignKey(gus_thread)
	created = models.DateTimeField(auto_now_add=True)
    	creator = models.ForeignKey(User, blank=True, null=True)
	def __unicode__(self):
		return u"%s - %s - %s" % (self.creator,self._thread,self._title)
	def short(self):
		return u"%s - %s\n%s" % (self.creator,self._title,self.created.strftime("%b %d, %I:%M %p"))
	short.allow_tags=True

	
	
