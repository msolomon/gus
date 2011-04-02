from imaplib import *
from django.db import models
from django.forms import ModelForm
from gus import settings

from gus.gus_widget.models import Widget
from gus.gus_groups.models import gus_group
from gus.gus_users.models import gus_user
from gus.gus_roles.models import gus_role

import sys
    
class News_upload_widget(models.Model):
    '''
    An email manager for a specific user
    '''
        
    def __unicode__(self):
        ''' Returns the name of the news feed (static)
            @rtype: string
            @return: name of news feed (static)
        '''
        return "NEWSFEED"
    
    def add_news(self, news):
        ''' Add a news item.
            @param news: the news item
            @type news: News_item
        '''
        news.feed = self
        news.save()
    
class News_item(models.Model):
    '''
        An individual news item.
    '''
    headline = models.CharField(max_length=100)
    shortdesc = models.TextField()
    content = models.TextField()
    date = models.DateField(blank=False)
    
    def __unicode__(self):
        ''' Returns the headline.
            @return: headline
            @rtype: string
        '''
        return unicode(headline)
    
    def delete_item(self):
        '''
            Deletes this news item.
        '''
        self.delete();

class News_form(ModelForm):
    class Meta:
        model = News_item
        fields = ('headline', 'shortdesc', 'content', 'date')