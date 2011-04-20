from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse ,HttpResponseRedirect
from django import forms
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from gus_roles.models import gus_role
from gus_users.models import gus_user
from gus_groups.models import gus_group
from gus_gallery.models import gus_gallery
from gus_gallery.models import gus_image
from gus_bill.models import bill
from gus_emailer.models import DBEmail, Emailer
from django.contrib.auth import authenticate,login
from django.contrib.auth.views import logout_then_login
import logging

class loginForm(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

def index(request):
    return HttpResponse('Hello World')
def welcome(request):
    if request.user.is_anonymous():
        return render_to_response('welcome.html',{
                                                  'groups':gus_group.objects.all().order_by('group_name')
                                                  },
                                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/users/profile')

def logoutView(request):
    return logout_then_login(request,'/login/')
    
def loginView(request):    

    if request.method == 'POST': # If the form has been submitted...
        form = loginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            un=form.cleaned_data['user'].lower()
            pw=form.cleaned_data['password']
            user = authenticate(username=un,
                                password=pw)
            if(user):
                login(request, user)
                try:
                    return HttpResponseRedirect(request.GET['next'])                    
                except:
                    return HttpResponseRedirect('/gus_test/User/Auth_Test/')
    else:
        form = loginForm()

    return render_to_response("users/login.html",{"form":form},context_instance=RequestContext(request))
    
def register(request):    
    return render_to_response("users/register.html")



#group_id will be used for our profile page
# beginnings of profile view that Chandler and Nathan are working on
@login_required
def profile(urlRequest):
    try:
        my_group_id = urlRequest.POST['groupSelect']
        my_group = gus_group.objects.get(pk=my_group_id)
    except:
        my_group=None
    
    
    my_self = urlRequest.user
    my_roles = gus_role.objects.with_user(my_self)
    
    my_images = []
    temp = []
    for b in my_roles:
        IMGS = b.group
        temp = gus_gallery.objects.filter(group = b.group)
        IMGS.my_images = len(temp.filter(user = my_self))
        my_images.append(IMGS)
    
    try:
        my_role = gus_role.objects.with_user_in_group(my_group, my_self)
    except:
        my_role = None
    my_bills = []
    for a in my_roles:
        AGRP = a.group
        AGRP.my_bills  = bill.objects.filter(group = a.group)
        my_bills.append(AGRP)
        
    Emailer(my_self).fetch_messages()
    
    unread_emails = DBEmail.objects.filter(gus_receivers=my_self).exclude(viewed=my_self).count()
    return render_to_response('users/profile.html',
                              {'roles':my_roles, 
                               'usr':my_self, 
                               'group':my_group, 
                               'role':my_role,
                               'bills':my_bills, 
                               'images':my_images,
                               'unread_emails': unread_emails}, 
                               context_instance=RequestContext(urlRequest))
    
def listing(urlRequest):
	return render_to_response('users/listing.html', {
         'groups':gus_group.objects.filter(parent_group=None).order_by('group_name'),
         },context_instance=RequestContext(urlRequest));



# Note to self: This function uncovered a naming inconsistency;
#    the group name is group_name, the user name is username, and the role name is just "name"
#    Bring up at next meeting


def users_groups(urlRequest,user_id):
    try:
        usr = gus_user.objects.get(pk=user_id)
    except:
        return HttpResponse("This User Does not exist<br/>")
    my_roles=gus_role.objects.with_user(usr)
    # Note to self: always include that last argument "context_instance=RequestContext(urlRequest)"
    return render_to_response('users/grouplisting.html', {'roles':my_roles}, context_instance=RequestContext(urlRequest))
