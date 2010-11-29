from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError 
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.http import HttpResponse , HttpResponseRedirect
from django.core.urlresolvers import url
from django import forms
from gus.gus_groups.models import *
from django.contrib import messages

def index(request):
	return HttpResponse("Gus Home")
#	return render_to_response('index_joran.html',{'lform':lform,'rform':rform},context_instance=RequestContext(request))
	
def super_manager(request):
	return HttpResponse("Super Manager!!!!")
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
	return HttpResponseRedirect(url('gus_groups.views.login'))	

class login_form(forms.Form):
	username=forms.CharField(max_length=50)
	password=forms.CharField(widget=forms.PasswordInput , max_length=50,min_length=6)
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


class reg_form(forms.Form):
	real_name=forms.CharField(max_length=50)
	email=forms.EmailField()
	username=forms.CharField(max_length=50)
	password=forms.CharField(widget=forms.PasswordInput , max_length=50,min_length=6)
	
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

def authenticate(username,password):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return None
	if user.check_password(password):return user	
	return None

def setup_and_save_tokens(request,user):
	try:
		u2=gus_user.objects.get(_user=user)
	except gus_user.DoesNotExist:
		return None
	u2._token =generate_token(user)	
	u2.save()
	try:
		CToken = user_token.objects.get(_user=u2)
	except user_token.DoesNotExist:
		CToken = user_token()
		CToken._user=u2
	CToken._token=u2._token
	CToken._username = user.username
	CToken.save()	
	request.session['user'] = CToken._token
	request.session.save()

def userauthenticated(request):
	key = request.session['user']
	u=gus_user.objects.get(_token=key)
	return u

	
def generate_token(user):
	import time
	from datetime import datetime
	import hashlib
	base=str(datetime.now())+user.password+user.username
	return  hashlib.sha1(base).hexdigest();
	
