from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from gus_forum.models import *
from gus_users.models import *
from gus_roles.models import *
from django import forms

class new_forum_form (forms.Form): 
	Name = forms.CharField(max_length = 25)
	Description = forms.CharField(widget = forms.Textarea)
#End

class new_thread_form (forms.Form):
	Name = forms.CharField(max_length = 25)
	Text = forms.CharField(widget = forms.Textarea)
#End

class new_post_form (forms.Form):
	Text = forms.CharField(widget = forms.Textarea)
#End

def index(request, group_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	request_for_group = gus_group.objects.get(pk = group_id)
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse("Invalid Permissions to View These Forums")
	#End

	groups_forums = forum.objects.filter(group = request_for_group)

	return render_to_response('forum/forums.html', {"forums":groups_forums, "group":request_for_group}, context_instance=RequestContext(request))
#End

def view_threads(request, group_id, forum_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	request_for_group = gus_group.objects.get(pk = group_id)
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse("Invalid Permissions to View These Threads")
	#End

	request_for_forum = forum.objects.get(pk = forum_id)
	forums_threads = forum_thread.objects.filter(forum = request_for_forum)

	return render_to_response('forum/threads.html', {"threads": forums_threads, "group":request_for_group, "forum":request_for_forum}, context_instance=RequestContext(request))
#End

def view_posts(request, group_id, forum_id, thread_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	request_for_group = gus_group.objects.get(pk = group_id)
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse("Invalid Permissions to View These Forums")
	#End

	request_for_forum = forum.objects.get(pk = forum_id)
	request_for_thread = forum_thread.objects.get(pk = thread_id)
	threads_posts = forum_post.objects.filter(thread = request_for_thread)

	return render_to_response('forum/posts.html', {"posts": threads_posts, "thread": request_for_thread, "group":request_for_group, "forum":request_for_forum}, context_instance=RequestContext(request))
#End

def add_forum(request, group_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	request_for_group = gus_group.objects.get(pk = group_id)
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permission_level < 1:
#		return HttpResponse("Invalid Permissions to Add a Forum")
	#End

	if request.method == 'POST':
		form = new_forum_form(request.POST)
		if form.is_valid():
			form.cleaned_data["Name"],
			form.cleaned_data["Description"]
			forum.objects.create_forum(form.cleaned_data["Name"], form.cleaned_data["Description"], request_for_group)
			return HttpResponseRedirect('/forum/%s' %group_id)
		#End
	#End
	else:
		form = new_forum_form() 
	#End

	return render_to_response('forum/add_forum.html', {"group":request_for_group, "form":form}, context_instance=RequestContext(request))
#End

def add_thread(request, group_id, forum_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	request_for_group = gus_group.objects.get(pk = group_id)
	request_for_forum = forum.objects.get(pk = forum_id)
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse("Invalid Permissions to Add a Thread")
	#End

	if request.method == 'POST':
		form = new_thread_form(request.POST)
		if form.is_valid():
			form.cleaned_data["Name"],
			form.cleaned_data["Text"]
			request_for_forum.CreateThread(form.cleaned_data["Name"], request.user, form.cleaned_data["Text"], request_for_forum)
#			return HttpResponseRedirect('/forum/%s/%s' %group_id %forum_id)
			return HttpResponseRedirect('/forum/%s' %group_id)
		#End
	#End
	else:
		form = new_thread_form() 
	#End

	return render_to_response('forum/add_thread.html', {"forum":request_for_forum, "form":form}, context_instance=RequestContext(request))
#End

def add_post(request, group_id, forum_id, thread_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	request_for_group = gus_group.objects.get(pk = group_id)
	request_for_thread = forum_thread.objects.get(pk = thread_id)
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse("Invalid Permissions to Add a Post")
	#End

	if request.method == 'POST':
		form = new_post_form(request.POST)
		if form.is_valid():
			form.cleaned_data["Text"]
			request_for_thread.CreatePost(request.user, form.cleaned_data["Text"])
#			return HttpResponseRedirect('/forum/%s/%s/%s' %group_id %forum_id %thread_id)
			return HttpResponseRedirect('/forum/%s' %group_id)
		#End
	#End
	else:
		form = new_post_form() 
	#End

	return render_to_response('forum/add_post.html', {"thread":request_for_thread, "form":form}, context_instance=RequestContext(request))
#End
