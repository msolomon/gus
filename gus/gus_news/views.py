from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from gus_news.models import *
from gus.gus_groups.utils import *
from gus_users.models import gus_user
from django import forms
from gus import settings
import bleach

@login_required
def upload_form(request):
	#if not request.user.is_authenticated():
	#	return HttpResponseRedirect('/login/')
	form = News_form()
	usr = request.user
	groups = getGroupsWithUser(usr)
	if request.method == 'POST':
		form = News_form(request.POST)
		if form.is_valid():
			# process the data in form.cleaned_data
			ni = News_item()
			ni.headline = form.cleaned_data['headline']
			ni.date = form.cleaned_data['date']
			ni.shortdesc = bleach.clean(form.cleaned_data['shortdesc'], tags=settings.BLEACH_ALLOWED_TAGS)
			ni.content = bleach.clean(form.cleaned_data['content'], tags=settings.BLEACH_ALLOWED_TAGS)
			ni.group = form.cleaned_data['group']
			ni.save()
			
			return render_to_response('news/upload-show.html', {
				'headline':form.cleaned_data['headline'],
				'date':form.cleaned_data['date'],
				'shortdesc':form.cleaned_data['shortdesc'],
				'content':form.cleaned_data['content']
			}, context_instance=RequestContext(request))
	else:
		form = News_form()
		gids = [user_group.id for user_group in groups if usr.has_group_perm(user_group, 'Can add gus_news')]
		form.fields['group'].queryset = gus_group.objects.filter(pk__in=gids)
	return render_to_response('news/upload.html', {
		'form':form
	}, context_instance=RequestContext(request))

@login_required
def all_news(request):
	#if not request.user.is_authenticated():
	#	return HttpResponseRedirect('/login/')
	user_groups = getGroupsWithUser(request.user) #[r.group for r in request.user.roles]
	allnews = News_item.objects.filter(group__in = user_groups)
	usr = request.user
	groups = getGroupsWithUser(usr)
	gids = [user_group.id for user_group in groups if usr.has_group_perm(user_group, 'Can add gus_news')]
	addlink = '';
	if (len(gids) > 0):
		addlink = '<a href="/news/_add">Add News Item</a>'
	#allnews = News_item.objects.all()
	return render_to_response('news/show.html', {
		'r':reversed(allnews),
		'addlink':addlink
	}, context_instance=RequestContext(request))