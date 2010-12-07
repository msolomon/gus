from gus.gus_groups.models import *
from django import forms
from django.db import models
# Create your models here.


class gus_forum(models.Model):
	_title = models.CharField(max_length=50)
	_group = models.ForeignKey(gus_group)
	def __unicode__(self):
		return self._title
	def group(self):
		return self._group
	def title(self):return self._title
	def num_posts(self): return sum([t.num_posts() for t in self.gus_thread_set.all()])
	def last_post(self):
	        if self.gus_thread_set.count():
         	   	last = None
            		for t in self.gus_thread_set.all():
                		l = t.last_post()
                		if l:
                    			if not last: last = l
                    			elif l.created > last.created: last = l
            	return last

class gus_thread(models.Model):
	_forum = models.ForeignKey(gus_forum)
	_title = models.CharField(max_length=50)
	created = models.DateTimeField(auto_now_add=True)
    	creator = models.ForeignKey(User, blank=True, null=True)
	def num_posts(self):return self.gus_message_set.count()
	def title(self): return self._title
	def forumid(self):return self._forum.id
	def group(self):return self._forum.group()
	def last_post(self):
		if self.gus_message_set.count():
			return self.gus_message_set.order_by("-created")[0]
	def __unicode__(self):
		return unicode(self.creator)+" - "+self._title

class gus_message(models.Model):
	_title  = models.CharField(max_length=50)
	_body   = models.TextField(max_length=10000)
	_thread = models.ForeignKey(gus_thread)
	created = models.DateTimeField(auto_now_add=True)
    	creator = models.ForeignKey(User, blank=True, null=True)
	def tid(self):return self._thread.id
	def title(self):return self._title
	def message(self): return self._body
	def group(self):
		return self._thread._forum.group()
	def pub_date(self,formatstring="%b %d, %I:%M %p"):
		return self.created.strftime(formatstring)

	def __unicode__(self):
		return u"%s - %s - %s" % (self.creator,self._thread,self._title)
	def short(self):
		return u"%s - %s\n%s" % (self.creator,self._title,self.pub_date())
	short.allow_tags=True

	
	
