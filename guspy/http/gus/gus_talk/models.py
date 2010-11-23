from django.db import models
from gus.gus_groups import *
# Create your models here.

class Board(models.Model):
	_group=models.OneToOneField(gus_group)
	_forums=models.OneToManyField(gus_forum)

class gus_forum(models.Model):
	_title=models.CharField(max_length=100)
	_topics=models.OneToManyField(gus_topic)
	_privacy=models.OneToManyField(gus_roles)
	def add_topic(self,gustopic):
		print "do something"

class gus_topic(models.Model):
	_title = models.CharField(max_length=100)
	_messages=models.OneToManyField(gus_message)
	def add_message(self,text):
		print "add a message to this topic"

class gus_message(models.Model):
	_author=models.ForeignKey(gus_user)
		
