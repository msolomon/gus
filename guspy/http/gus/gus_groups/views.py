###
# Joran Beasle
# View Controller for Gus Python Team
# CS383  Fall2010
#    This collection of functions manages the views that are associated with gus users
#  	It is dependent on gus_groups  models  (gus_user,gus_group,gus_roles)
#	It is also dependent on gus_groups forms which contains the form definitions for various views
#	It also utilizes some helper functions (found in file)
###

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError 
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.http import HttpResponse , HttpResponseRedirect
from django import forms
from gus.gus_groups.models import *
from gus.gus_groups.forms import *
from django.contrib import messages

def index(request):
	return HttpResponse("Gus Home")

def dummy_setup(request,file=None):
	if not file return HttpResponse('No File Supplied')
	resp = "Created User <%s>"%"Joran"
	return HttpResponse(resp)	

class role_form(forms.Form):
	users = forms.CharField(max_length=100)
	
def groupadmin(request,gid):
	rf=role_form()		
	return render_to_response('gus_groups/group_admin.html'		
		,{'role_form':rf,'role':1}
		,context_instance=RequestContext(request))
def super_user_manager(request):
	return HttpResponse("Super UManager!!!!")
def super_group_manager(request):
	return HttpResponse("Super GManager!!!!")

class new_group_form(forms.Form):
	group_name = forms.CharField(max_length=50)
	ownerid = forms.IntegerField()
def view_group(request,gid):
	group=gus_group.objects.get(id=gid)
	members = gus_roles.objects.filter(gid=group)
	return render_to_response('gus_groups/group_view.html',{'users':members,'group':group},context_instance=RequestContext(request))
	
def create_group(request):
	usr = userauthenticated(request)
	if request.method == 'POST': # If the form has been submitted...
		gf=new_group_form(request.POST)
		if gf.is_valid():
			if gus_group.objects.filter(group_name=gf.cleaned_data['group_name']).count() > 0 :
				gf._errors['group_name']= (u'This Group Name Is Already Taken.',)
			else:
				g1 = gus_group(group_name=gf.cleaned_data['group_name'])
				g1.save()		
				r=gus_roles(gid=g1,role_name="Owner")
				r.save()
				r.uid.add(usr.id)
				return HttpResponse("OK Create Group "+gf.cleaned_data['group_name'])
	else:
		gf = new_group_form()
	
	return render_to_response('gus_groups/group_register.html',{'user':usr,'group_form':gf},context_instance=RequestContext(request))
	
def profile(request):
	usr = userauthenticated(request)
	groups = gus_roles.objects.filter(uid=usr)
	return render_to_response('gus_groups/user_profile.html',{'user':usr,'groups':groups},context_instance=RequestContext(request))
	
def user_detail_view(request,user_id):
	usr=gus_roles.objects.get(uid=user_id)
	return HttpResponse("View User Detail For User "+usr.uid.all()[0]._user.username)
	

def logout(request):
	try:
		del request.session['user']
	except:
		1
	return HttpResponseRedirect('/login/')

def login(request):
	if request.method == 'POST': # If the form has been submitted...
		lform = login_form(request.POST)
		if(lform.is_valid()):
			usr=do_login(lform.cleaned_data['username'],lform.cleaned_data['password'])
			if (usr):
				setup_and_save_tokens(request,usr)
				return HttpResponseRedirect('/profile/')
			else:
				messages.error(request,"USERNAME/PASSWORD INVALID")
				return HttpResponseRedirect('/login/')
	else:
		lform=login_form()
	return render_to_response('gus_groups/user_login.html',{'lform':lform},context_instance=RequestContext(request))


	
def register(request):
	if request.method == 'POST': # If the form has been submitted...
		rform = reg_form(request.POST)
		if(rform.is_valid()):
			from django.contrib.auth.models import User
			try:
				u = User.objects.create_user(
					rform.cleaned_data['username'], 
					rform.cleaned_data['email'], 
					rform.cleaned_data['password'])
				names = rform.cleaned_data['real_name'].split()
				u.first_name = names[0]
				if(len(names)>1):
					u.last_name = names[1]
				u.save()
			except IntegrityError:
				rform._errors['username']= (u'This Username Is Already Taken.',)
				return render_to_response('gus_groups/register_user.html',{'rform':rform},context_instance=RequestContext(request))
			gu = gus_user(_user=u)
			gu.save()						
			messages.success(request,"Successfully Registered You May Now Login")
			return HttpResponseRedirect('/login/')
	else: #else no form submitted create empty form
		rform=reg_form()
	return render_to_response('gus_groups/register_user.html',{'rform':rform},context_instance=RequestContext(request))

def do_login(username,password):
	user = authenticate(username, password)
	print user
	if user is not None:
    		if user.is_active:
        		return user
    		else: 
			return -1
	



def group_module(request,group_slug,module_slug):
	return HttpResponse("Viewing "+module_slug+" For <b>"+group_slug)



def import_users(request):
	return HttpResponse("Import Users")	
