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

	request_for_forum = gus_forum.objects.get(pk = forum_id)
	forums_threads = gus_forum.forum_thread.objects.filter(group = request_for_group, forum = request_for_forum)

	return render_to_response('forum/threads.html', {"threads": forums_threads}, context_instance=RequestContext(request))
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

	request_for_forum = gus_forum.objects.get(pk = forum_id)
	request_for_thread = gus_thread.objects.get(pk = thread_id)
	threads_posts = gus_forum.forum_post.objects.filter(group = request_for_group, forum = request_for_forum, thread = request_for_thread)

	return render_to_response('forum/posts', {"posts": threads_posts}, contect_instance=RequestContect(request))
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
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse("Invalid Permissions to Add a Thread")
	#End

	request_for_forum = gus_forum.objects.get(pk = forum_id)
	form = new_thread_form()

	return render_to_response('forum/add_thread.html', {"forum":request_for_forum, "form":form}, context_instance=RequestContext(request))
#End

def add_post(request, group_id, forum_id, thread_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	request_for_group = gus_group.objects.get(pk = group_id)
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse("Invalid Permissions to Add a Post")
	#End

	request_for_thread = gus_forum.objects.get(pk = thread_id)
	form = new_post_form()

	return render_to_response('forum/add_post.html', {"thread":request_for_thread, "form":form}, context_instance=RequestContext(request))
#End
