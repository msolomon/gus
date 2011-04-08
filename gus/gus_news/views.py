from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from gus_news.models import *
from gus.gus_groups.utils import *
from gus_users.models import gus_user
from django import forms

def upload_form(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	form = News_form()
	if request.method == 'POST':
		form = News_form(request.POST)
		if form.is_valid():
			# process the data in form.cleaned_data
			ni = News_item()
			ni.headline = form.cleaned_data['headline']
			ni.date = form.cleaned_data['date']
			ni.shortdesc = form.cleaned_data['shortdesc']
			ni.content = form.cleaned_data['content']
			ni.group = form.cleaned_data['group']
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
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	user_groups = getGroupsWithUser(request.user) #[r.group for r in request.user.roles]
	allnews = News_item.objects.filter(group__in = user_groups)
	#allnews = News_item.objects.all()
	return render_to_response('news/show.html', {
		'r':allnews
	}, context_instance=RequestContext(request))