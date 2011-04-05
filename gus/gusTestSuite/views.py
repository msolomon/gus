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
    return render_to_response('users/info.html',{},
                              context_instance=RequestContext(urlRequest))
def addGroup(urlRequest):
    
    from gus.gus_groups.utils import createNewGroup
    from gus.gusTestSuite.forms import SimpleGroupAddForm
    
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
                                 'submiturl':'/gus_test/Group/Add/',
                                 'enctype':'multipart/form-data',
                                 'form':form,
                                 'title':'Add New Group',
                                 'btnlabel':'Create Group',
                                },
                                context_instance=RequestContext(urlRequest)
                              );

def editUser(urlRequest, user_id):
    #get our user
    usr = gus_user.objects.get(pk=user_id)
    #setup our form
    if urlRequest.method == 'POST': # If the form has been submitted...
        form = SimpleUserAddForm(urlRequest.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            usr.username=form.cleaned_data['username']
            usr.email=form.cleaned_data['email']
            usr.save()
            usr.set_password(form.cleaned_data['password'])
                        
            return HttpResponseRedirect('/gus_test/') # Redirect after POST
    else:
        form = SimpleUserAddForm({'username':usr.username,'email':usr.email
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


def editGroup(urlRequest, group_id):
    from gus.gus_groups.utils import getGroupRoles
    from gus.gusTestSuite.forms import SimpleAddUserToGroup
   
    if urlRequest.method == 'POST':
        usr = gus_user.objects.get(pk=int(urlRequest.POST['new_member']))
        role = gus_role.objects.get(pk=int(urlRequest.POST['role']))
        role.users.add(usr)
        #return HttpResponse("New User ID : %s " % new_mem_id)
    group = gus_group.objects.get(pk=group_id)
    form_addUser = SimpleAddUserToGroup(group)    
    return render_to_response('groups/manageGroup.html',
        { 'group':group, 'roles':getGroupRoles(group),
          'formAddUser':form_addUser},
          context_instance=RequestContext(urlRequest)
          )
    return HttpResponse('Manage Group : %s ' % group)

def deleteUser(urlRequest, user_id):
    user = gus_user.objects.get(pk=user_id)
    return HttpResponse('Delete User : %s ' % user)
def deleteGroup(urlRequest, group_id):
    group = gus_group.objects.get(pk=group_id)
    return HttpResponse('Delete Group : %s ' % group)

def removeUserFromRole(urlRequest, user_id, role_id):
    user = gus_user.objects.get(pk=user_id)
    role = gus_role.objects.get(pk=role_id)
    role.users.remove(user)
    return HttpResponseRedirect('/gus_test/Role/Edit/%s'%role_id)

def deleteRole(urlRequest, role_id):
    role = gus_role.objects.get(pk=role_id)
    role.delete() #Needs help in terms of uniqueness
    return HttpResponseRedirect('/gus_test/')

def editRole(urlRequest, role_id):
  
    role = gus_role.objects.get(pk=role_id)

   
    
    return render_to_response('groups/manageRole.html',
                       {
                         'role':role,
                        
                       },context_instance=RequestContext(urlRequest)
                       )


def addUser(urlRequest):
    
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
                                 'submiturl':'/gus_test/User/Add/',
                                 'encType':'multipart/form-data',
                                 'form':form,
                                 'title':'Add New User',
                                 'btnlabel':'Create User',
                                },
                                context_instance=RequestContext(urlRequest)
                              );
                              
def viewUser(urlRequest,user_id):
    try:
        usr = gus_user.objects.get(pk=user_id)
    except:
        return HttpResponse("This User Does not exist<br/>")
    return render_to_response('test/viewUser.html',
                                {
                                 'usr':usr,
                                 'roles':gus_role.objects.with_user(usr),
                                },
                                context_instance=RequestContext(urlRequest)
                              );
def createRole(urlRequest,group_id):
    group = gus_group.objects.get(pk=group_id)
    if urlRequest.method == 'POST':
        form = RoleCreateForm(urlRequest.POST)
	if form.is_valid():
	    role = gus_role.objects.create_role(group,form.cleaned_data['role_name'])
	    if form.cleaned_data['is_superUser'] == True:
		role._role_permission_level = 1
	    [role._role_permissions.permissions.add(r) for r in form.cleaned_data['role_permissions']]
    else:
        form = RoleCreateForm({'id':group_id})
	
#    return HttpResponse("WIP")
    return render_to_response('test/form.html',
                                {
                                 'submiturl':('/gus_test/Role/New/%s/'%group_id),
                                 'encType':'multipart/form-data',
                                 'form':form,
                                 'title':'Create Role for %s'%group.group_name,
                                 'btnlabel':'Create Role',
                                },
                                context_instance=RequestContext(urlRequest)
                              )
def editRolePerms(urlRequest,role_id):
    role = gus_role.objects.get(pk=role_id)
    if urlRequest.method == 'POST':
        form = RolePermissionForm(urlRequest.POST)
	if form.is_valid():
	    role._role_permissions.permissions.clear()
	    role._role_permission_level = int(form.cleaned_data['is_superUser'])
	    [role._role_permissions.permissions.add(r) for r in form.cleaned_data['role_permissions']]
	    role.save()
    else:
	if role._role_permission_level == 1:
	    is_superUser = True
	else:
	    is_superUser = False
	role_permissions = role._role_permissions.permissions.all()
	data = {'id':role_id, 'is_superUser':is_superUser, 'role_permissions':role_permissions}
        form = RolePermissionForm(data)

    #return HttpResponse("WIP")
    
    return render_to_response('test/form.html',
                                {
                                 'submiturl':('/gus_test/Role/EditPerms/%s/'%role_id),
                                 'encType':'multipart/form-data',
                                 'form':form,
                                 'title':'Edit Permissions For Role %s'%role.name,
                                 'btnlabel':'Save Role',
                                },
                                context_instance=RequestContext(urlRequest)
                              )
