from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from gus_news.models import *
from gus_users.models import gus_user
from django import forms

def upload_form(request):
	form = News_form()
	if request.method == 'POST':
		form = News_form(request.POST)
		if form.is_valid():
			# process the data in form.cleaned_data
			ni = form.save(commit=false)
			ni.save()
			
			return render_to_response('news/upl-test.html', {
				'headline':form.cleaned_data['headline'],
				'date':form.cleaned_data['date'],
				'shortdesc':form.cleaned_data['shortdesc'],
				'content':form.cleaned_data['content']
			}, context_instance=RequestContext(request))
	else:
		form = News_form()
	return render_to_response('news/upload.html', {
		'form':form
	}, context_instance=RequestContext(request))

def all_news(request):
	allnews = News_upload_widget.get_all_news()
	r = ""
	for ni in allnews.reverse():
		r += "<h4>" +  ni.headline + "</h4><i>" + ni.date + "</i><br /><br /><i>" + ni.shortdesc + "</i><br /><br />" + ni.content + "<br /><br /><br />"
	return render_to_response('news/show.html', {
		'r':r
	}, context_instance=RequestContext(request))