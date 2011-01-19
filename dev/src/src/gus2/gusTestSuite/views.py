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
from django.shortcuts import render_to_response
from django.template import  RequestContext #,Context, loader
from django.http import HttpResponseRedirect ,HttpResponse  
from django.core.urlresolvers import reverse
#from django import forms
#from gus.gus_groups.models import *
#from gus.gus_groups.forms import *
#from django.contrib import messages
from gus2.gus_users.models import gus_user
from gus2.gus_groups.models import gus_group
from gus2.gus_roles.models import gus_role


def index(urlRequest):
    
    #from django.contrib.auth.forms import UserCreationForm
    #from gus2.gusTestSuite.forms import SimpleAddUserToGroup
    #return HttpResponse(SimpleGroupAddForm().as_p())
    return render_to_response('test/welcome.html',{
         'users':gus_user.objects.all(),
         'groups':gus_group.objects.all(),                                          
         });
                              
def addGroup(urlRequest):
    
    from gus2.gus_groups.utils import createNewGroup
    from gus2.gusTestSuite.forms import SimpleGroupAddForm
    
    #setup our form
    if urlRequest.method == 'POST': # If the form has been submitted...
        form = SimpleGroupAddForm(urlRequest.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            createNewGroup(
                    form.cleaned_data['group_owner'],
                    form.cleaned_data['group_name'],
                    form.cleaned_data['group_description'], 
                    ""
                    )
            
            return HttpResponseRedirect('/gus_test/') # Redirect after POST
    else:
        form = SimpleGroupAddForm() # An unbound form

    
    return render_to_response('test/form.html',
                                {
                                 'submiturl':reverse('gus2.gusTestSuite.views.addGroup'),
                                 'enctype':'multipart/form-data',
                                 'form':form,
                                 'title':'Add New Group',
                                 'btnlabel':'Create Group',
                                },
                                context_instance=RequestContext(urlRequest)
                              );

def editUser(urlRequest,user_id):
    user = gus_user.objects.get(pk=user_id)
    return HttpResponse('Manage User : %s ' % user)

def editGroup(urlRequest,group_id):
    from gus2.gus_groups.utils import getGroupRoles
    from gus2.gusTestSuite.forms import SimpleAddUserToGroup
   
    if urlRequest.method == 'POST':
        usr = gus_user.objects.get(pk=int(urlRequest.POST['new_member']))
        role = gus_role.objects.get(pk=int(urlRequest.POST['role']))
        role.users.add(usr)
        #return HttpResponse("New User ID : %s " % new_mem_id)
    group = gus_group.objects.get(pk=group_id)
    form_addUser = SimpleAddUserToGroup(group)    
    return render_to_response('groups/manageGroup.html',
        { 'group':group,'roles':getGroupRoles(group),
          'formAddUser':form_addUser},
          context_instance=RequestContext(urlRequest)
          )
    return HttpResponse('Manage Group : %s ' % group)

def deleteUser(urlRequest,user_id):
    user = gus_user.objects.get(pk=user_id)
    return HttpResponse('Delete User : %s ' % user)
def deleteGroup(urlRequest,group_id):
    group = gus_group.objects.get(pk=group_id)
    return HttpResponse('Delete Group : %s ' % group)

def removeUserFromRole(urlRequest,user_id,role_id):
    user = gus_user.objects.get(pk=user_id)
    role = gus_role.objects.get(pk=role_id)
    role.users.remove(user)
    return HttpResponseRedirect(
            reverse('gus2.gusTestSuite.views.editRole',args=[role_id])
            )    
def editRole(urlRequest,role_id):
  
    role = gus_role.objects.get(pk=role_id)
   
    
    return render_to_response('groups/manageRole.html',
                       {
                         'role':role,
                        
                       }
                       )


def addUser(urlRequest):
    from gus2.gusTestSuite.forms import SimpleUserAddForm
    #setup our form
    if urlRequest.method == 'POST': # If the form has been submitted...
        form = SimpleUserAddForm(urlRequest.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            gus_user.objects.create_user(
                            form.cleaned_data['username'],
                            form.cleaned_data['email'],
                            form.cleaned_data['password'],
                        )
            return HttpResponseRedirect('/gus_test/') # Redirect after POST
    else:
        form = SimpleUserAddForm() # An unbound form


    return render_to_response('test/form.html',
                                {
                                 'submiturl':reverse('gus2.gusTestSuite.views.addUser'),
                                 'encType':'multipart/form-data',
                                 'form':form,
                                 'title':'Add New User',
                                 'btnlabel':'Create User',
                                },
                                context_instance=RequestContext(urlRequest)
                              );
                              
