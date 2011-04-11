from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from gus_forum.models import *
from gus_users.models import *
from gus_roles.models import *

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

class delete_post_form (forms.Form):
	Reason = forms.CharField(widget = forms.Textarea)
#End

def index(request, group_id):
	"""
	"""

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End

	groups_forums = forum.objects.filter(group = request_for_group)
	
	return render_to_response('forum/forums.html', {"forums":groups_forums, "group":request_for_group}, context_instance=RequestContext(request))
#End

def view_threads(request, group_id, forum_id):
	"""
	"""

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
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

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
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

@login_required
def add_forum(request, group_id):
	"""
	"""

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	if not request.user.has_group_perm(request_for_group, 'Can add forum'):
		return HttpResponse("You are not allowed to add a forum to this group.")
	#End

	if request.method == 'POST':
		form = new_forum_form(request.POST)
		if form.is_valid():
			form.cleaned_data["Name"],
			form.cleaned_data["Description"]
			exists = forum.objects.filter(forum_name = form.cleaned_data["Name"], group = request_for_group)
			if len(exists) > 0:
				return HttpResponse("A forum already exists with this name.")
			#End
			forum.objects.create_forum(form.cleaned_data["Name"], form.cleaned_data["Description"], request_for_group)
			return HttpResponseRedirect('/forum/%s' %group_id)
		#End
	#End
	else:
		form = new_forum_form() 
	#End

	return render_to_response('forum/add_forum.html', {"group":request_for_group, "form":form}, context_instance=RequestContext(request))
#End

@login_required
def add_thread(request, group_id, forum_id):
	"""
	"""

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	if not request.user.has_group_perm(request_for_group, 'Can add forum_thread'):
		return HttpResponse("You are not allowed to post a thread to this group's forums.")
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
				last_thread = forum_thread.objects.filter(forum = request_for_forum).order_by('-date_created')
				request_for_thread = forum_thread.objects.get(pk = last_thread[0].id)
			except:
				return HttpResponse('Thread Was Not Created!')
			#End
			request_for_thread.CreatePost(request.user, form.cleaned_data["Text"])
			return HttpResponseRedirect('/forum/%s/%s' % (group_id, forum_id))
		#End
	#End
	else:
		form = new_thread_form() 
	#End

	return render_to_response('forum/add_thread.html', {"group":request_for_group, "forum":request_for_forum, "form":form}, context_instance=RequestContext(request))
#End

@login_required
def add_post(request, group_id, forum_id, thread_id):
	"""
	"""

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	if not request.user.has_group_perm(request_for_group, 'Can add forum_post'):
		return HttpResponse("You are not allowed to post replys to this group's threads.")
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

	return render_to_response('forum/add_post.html', {"group":request_for_group, "forum":request_for_forum, "thread":request_for_thread, "form":form}, context_instance=RequestContext(request))
#End

@login_required
def delete_forum(request, group_id, forum_id):
	"""
	"""

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	if not request.user.has_group_perm(request_for_group, 'Can delete forum'):
		return HttpResponse("You are not allowed to delete this group's forums.")
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	#End

	request_for_forum.delete()
	return HttpResponseRedirect('/forum/%s/' % group_id)
#End

@login_required
def delete_thread(request, group_id, forum_id, thread_id):
	"""
	"""

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	if not request.user.has_group_perm(request_for_group, 'Can delete forum_thread'):
		return HttpResponse("You are not allowed to delete this group's threads.")
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

@login_required
def delete_post(request, group_id, forum_id, thread_id, post_id):
	"""
	"""

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	if not request.user.has_group_perm(request_for_group, 'Can delete forum_post'):
		return HttpResponse("You are not allowed to delete this group's posts.")
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

	if request.method == 'POST':
		form = delete_post_form(request.POST)
		if form.is_valid():
			form.cleaned_data["Reason"]
			request_for_post.EditPost("Post Deleted by %s. Reason: %s" % (request.user.username, form.cleaned_data["Reason"]))
			return HttpResponseRedirect('/forum/%s/%s/%s' % (group_id, forum_id, thread_id))
		#End
	#End
	else:
		form = delete_post_form()
	#End

	return render_to_response('forum/delete_post.html', {"group":request_for_group, "forum":request_for_forum, "thread":request_for_thread, "post":request_for_post, "form":form}, context_instance=RequestContext(request))
#End

@login_required
def edit_forum(request, group_id, forum_id):
	"""
	"""

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	if not request.user.has_group_perm(request_for_group, 'Can change forum'):
		return HttpResponse("You are not allowed to edit this group's forums.")
	#End

	try:
		request_for_forum = forum.objects.get(pk = forum_id)
	except:
		return HttpResponse('Forum Not Found!')
	#End

	if request.method == "POST":
		form = new_forum_form(request.POST, instance=request_for_forum)
		if form.is_valid():
			forum = form.save(commit=False)
			return HttpResponseRedirect('/forum/%s' %group_id)
		#End
	#End
	else:
		form = new_forum_form()
	#End

	return render_to_response('forum/edit_forum.html', {"group":request_for_group, "forum":request_for_forum, "form":form}, context_instance=RequestContext(request))
#End

@login_required
def edit_post(request, group_id, forum_id, thread_id, post_id):
	"""
	"""

	try:
		request_for_group = gus_group.objects.get(pk = group_id)
	except:
		return HttpResponse('Group Not Found!')
	#End
	if not request.user.has_group_perm(request_for_group, 'Can change forum_post'):
		return HttpResponse("You are not allowed to edit this group's posts.")
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
	
	if not request.user == request_for_post.user:
		return HttpResponse("You are only allowed to edit your own posts.")
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