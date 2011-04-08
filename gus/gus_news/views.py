from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from gus_news.models import *
from gus_users.models import gus_user
from django import forms

def upload_form(request):
	form = News_form()
	#headline = forms.CharField(max_length = 64)
	#shortdesc = forms.CharField(max_length=1000, widget=forms.Textarea)
	#content = forms.CharField(max_length=10000, widget=forms.Textarea)
	#date = forms.DateField('%b %d, %Y')
	#return render_to_response("news/upload.html",
	#						{   'news_form':form,
	#							'headline': headline, 
	#							'date': date, 
	#							'shortdesc': shortdesc, 
	#							'content': content}, 
	#							context_instance=RequestContext(request))
	if request.method == 'POST':
		form = News_form(request.POST)
		if form.is_valid():
			# process the data in form.cleaned_data
			# ...
			return HttpResponseRedirect('/')
		else:
			form = News_form()
		return render_to_response('news/upload.html', {
			'form':form,
		})
