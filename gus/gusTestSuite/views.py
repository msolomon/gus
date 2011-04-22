###
# Joran Beasle
# View Controller for Gus Python Team
# CS383  Fall2010
#    This collection of functions manages the views that are associated with gus users
#      It is dependent on gus_groups  models  (gus_user,gus_group,gus_roles)
#    It is also dependent on gus_groups forms which contains the form definitions for various views
#    It also utilizes some helper functions (found in file)
###

#from django.core.exceptions import ObjectDoesNotExist
#from django.db import IntegrityError 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import  RequestContext #,Context, loader
from django.http import HttpResponseRedirect , HttpResponse  
from django.core.urlresolvers import reverse
#from django import forms
#from gus.gus_groups.models import *
#from gus.gus_groups.forms import *
#from django.contrib import messages
from gus import settings
from gus.gus_users.models import gus_user
from gus.gus_groups.models import gus_group
from gus.gus_roles.models import gus_role

from gus.gusTestSuite.forms import *

@login_required
def index(urlRequest):
    
    #from django.contrib.auth.forms import UserCreationForm
    #from gus.gusTestSuite.forms import SimpleAddUserToGroup
    #return HttpResponse(SimpleGroupAddForm().as_p())
    return render_to_response('test/welcome.html', {
         'users':gus_user.objects.all(),
         'groups':gus_group.objects.all(),
         },context_instance=RequestContext(urlRequest));

def authUser(urlRequest):
    return HttpResponseRedirect('/users/profile')

@login_required
def editUser(urlRequest, user_id):
    #get our user
    usr = gus_user.objects.get(pk=user_id)
    #setup our form
    if urlRequest.method == 'POST': # If the form has been submitted...
        form = SimpleUserEditForm(urlRequest.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            usr.username=form.cleaned_data['username']
            usr.email=form.cleaned_data['email']
            usr.save()
            usr.set_password(form.cleaned_data['password'])
                        
            return HttpResponseRedirect('/users/profile') # Redirect after POST
    else:
        form = SimpleUserEditForm({'username':usr.username,'email':usr.email
                              ,'id':usr.id,'password':usr._user.password}) 
        # Default Edit Form
    
    
    #return HttpResponse()
    return render_to_response('test/form.html',
                                {
                                 'submiturl':'/gus_test/User/Edit/%s/'%user_id,
                                 'enctype':'multipart/form-data',
                                 'form':form,
                                 'title':'Edit %s'%usr.username,
                                 'btnlabel':'Save Changes',
                                },
                                context_instance=RequestContext(urlRequest)
                              );


@login_required
def deleteUser(urlRequest, user_id):
    user = gus_user.objects.get(pk=user_id)
    return HttpResponse('Delete User : %s ' % user)

 
 
#@login_required # you need to be able to register without being logged in
def addUser(urlRequest):
    
    #setup our form
    if urlRequest.method == 'POST': # If the form has been submitted...
        form = SimpleUserAddForm(urlRequest.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            usr = gus_user.objects.create_user(
                            form.cleaned_data['username'],
                            form.cleaned_data['email'],
                            form.cleaned_data['password'],
                        )
            usr._user.first_name=form.cleaned_data['real_name']
            usr._user.save()
            return HttpResponseRedirect('/users/profile') # Redirect after POST

    else:
        form = SimpleUserAddForm() # An unbound form

    return render_to_response('test/form.html',
                                {
                                 'submiturl':'/gus_test/User/Add/',
                                 'encType':'multipart/form-data',
                                 'form' : form,
                                 'title':'Register New User',
                                 'btnlabel':'Create User',
                                },
                                context_instance=RequestContext(urlRequest)
                              );
