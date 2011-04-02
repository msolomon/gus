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

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
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

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse('Invalid Permissions to View These Threads')
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	#End

	forums_threads = forum_thread.objects.filter(forum = request_for_forum)

	return render_to_response('forum/threads.html', {"threads": forums_threads, "forum":request_for_forum, "group":request_for_group}, context_instance=RequestContext(request))
#End

def view_posts(request, group_id, forum_id, thread_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse('Invalid Permissions to View These Forums')
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	try:
		request_for_thread = forum_thread.objects.get(pk = thread_id)
	except:
		return HttpResponse('Thread Not Found!')
	#End

	threads_posts = forum_post.objects.filter(thread = request_for_thread)

	return render_to_response('forum/posts.html', {"posts": threads_posts, "thread": request_for_thread, "forum":request_for_forum, "group":request_for_group}, context_instance=RequestContext(request))
#End

def add_forum(request, group_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permission_level < 1:
#		return HttpResponse('Invalid Permissions to Add a Forum')
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

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse('Invalid Permissions to Add a Thread')
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	#End

	if request.method == 'POST':
		form = new_thread_form(request.POST)
		if form.is_valid():
			form.cleaned_data["Name"],
			form.cleaned_data["Text"]
			request_for_forum.CreateThread(form.cleaned_data["Name"], request.user, form.cleaned_data["Text"], request_for_forum)
			try:
				last_thread = forum_thread.objects.filter(forum = request_for_forum).order_by('date_created') #This
				request_for_thread = forum_thread.objects.get(pk = last_thread[0].id)						  #Doesn't
			except:
				return HttpResponse('Thread Was Not Created!')												  #Quite
			#End
			request_for_thread.CreatePost(request.user, form.cleaned_data["Text"])							  #Work
			return HttpResponseRedirect('/forum/%s/%s' % (group_id, forum_id))
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

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse('Invalid Permissions to Add a Post')
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	try:
		request_for_thread = forum_thread.objects.get(pk = thread_id)
	except:
		return HttpResponse('Thread Not Found!')
	#End

	if request.method == 'POST':
		form = new_post_form(request.POST)
		if form.is_valid():
			form.cleaned_data["Text"]
			request_for_thread.CreatePost(request.user, form.cleaned_data["Text"])
			return HttpResponseRedirect('/forum/%s/%s/%s' % (group_id, forum_id, thread_id))
		#End
	#End
	else:
		form = new_post_form() 
	#End

	return render_to_response('forum/add_post.html', {"thread":request_for_thread, "form":form}, context_instance=RequestContext(request))
#End

def delete_forum(request, group_id, forum_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permission_level < 1:
#		return HttpResponse('Invalid Permissions to Delete a Forum')
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	#End

	request_for_forum.delete()
	return HttpResponseRedirect('/forum/%s/' % group_id)
#End

def delete_thread(request, group_id, forum_id, thread_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permission_level < 1:
#		return HttpResponse('Invalid Permissions to Delete a Thread')
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	try:
		request_for_thread = forum_thread.objects.get(pk = thread_id)
	except:
		return HttpResponse('Thread Not Found!')
	#End

	request_for_thread.delete()
	return HttpResponseRedirect('/forum/%s/%s/' % (group_id, forum_id))
#End

def delete_post(request, group_id, forum_id, thread_id, post_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse('Invalid Permissions to Delete a Post')
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	try:
		request_for_thread = forum_thread.objects.get(pk = thread_id)
	except:
		return HttpResponse('Thread Not Found!')
	try:
		request_for_post = forum_post.objects.get(pk = post_id)
	except:
		return HttpResponse('Post Not Found!')
	#End

	request_for_post.delete()
	return HttpResponseRedirect('/forum/%s/%s/%s/' % (group_id, forum_id, post_id))
#End

def edit_forum(request, group_id, forum_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse('Invalid Permissions to Delete a Post')
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	#End

	if request.method == "POST":
		form = new_forum_form(request.POST, instance=request_for_forum)
		if form.is_valid():
			forum = form.save()
			return HttpResponseRedirect('/forum/%s' %group_id)
		#End
	#End
	else:
		form = new_forum_form()
	#End

	return render_to_response('forum/edit_forum.html', {"group":request_for_group, "forum":request_for_forum, "form":form}, context_instance=RequestContext(request))
#End

def edit_post(request, group_id, forum_id, thread_id, post_id):
	"""
	"""

	if request.user.is_anonymous():
		return HttpResponseRedirect('/login/')
	#End

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	role_in_group = gus_role.objects.with_user_in_group(request_for_group, request.user)
#	if not role_in_group || role_in_group._role_permissions_level == 1:
#		return HttpResponse('Invalid Permissions to Delete a Post')
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	try:
		request_for_thread = forum_thread.objects.get(pk = thread_id)
	except:
		return HttpResponse('Thread Not Found!')
	try:
		request_for_post = forum_post.objects.get(pk = post_id)
	except:
		return HttpResponse('Post Not Found!')
	#End

	if request.method == "POST":
		form = new_post_form(request.POST, instance=request_for_post)
		if form.is_valid():
			post = form.save()
			return HttpResponseRedirect('/forum/%s/%s/%s/' % (group_id, forum_id, post_id))
		#End
	#End
	else:
		form = new_post_form()
	#End

	return render_to_response('forum/edit_post.html', {"group":request_for_group, "forum":request_for_forum, "thread":request_for_thread, "post":request_for_post, "form":form}, context_instance=RequestContext(request))
#End