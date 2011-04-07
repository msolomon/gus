from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from gus_news.models import *
from gus_users.models import gus_user
from django import forms

def upload_form(request, headline, date, shortdesc, content):
	form = News_form()
	#headline = forms.CharField(max_length = 64)
	#shortdesc = forms.CharField(max_length=1000, widget=forms.Textarea)
	#content = forms.CharField(max_length=10000, widget=forms.Textarea)
	#date = forms.DateField('%b %d, %Y')
	return render_to_response("news/upload.html",
                            {   'news_form':form,
                                'headline': headline, 
                                'date': date, 
                                'shortdesc': shortdesc, 
                                'content': content}, 
                                context_instance=RequestContext(request))
