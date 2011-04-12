from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import  RequestContext #,Context, loader
from django.http import HttpResponseRedirect , HttpResponse
from django.core.urlresolvers import reverse

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
    data ={}
    usr=urlRequest.user
    grps = [r.group for r in gus_role.objects.with_user(usr)]
    data['user']=usr
    data['groups']=[{'group':g,'candeletegroup':usr.has_group_perm(g,'Can delete group')} for g in grps]

    #return HttpResponse(data['groups'][0].group_name)
    return render_to_response('test/welcome2.html', data
         #'urls':{'delete':'/gus_test/Group/Delete/%s/'},
         ,context_instance=RequestContext(urlRequest));

                                 
@login_required
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

@login_required
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
@login_required
def viewGroup(urlRequest, group_id):
    from gus.gusTestSuite.forms import SimpleAddUserToGroup

    if urlRequest.method == 'POST':
        usr = gus_user.objects.get(pk=int(urlRequest.POST['new_member']))
        role = gus_role.objects.get(pk=int(urlRequest.POST['role']))
        role.users.add(usr)
    group = gus_group.objects.get(pk=group_id)
    form_addUser = SimpleAddUserToGroup(group)
    role=gus_role.objects.with_user_in_group(group,urlRequest.user)
    roles = group.roles

    my_perms={
           'adduser':urlRequest.user.has_group_perm(group,'Can add user'),
           'deluser':urlRequest.user.has_group_perm(group,'Can delete user'),
           'edituser':urlRequest.user.has_group_perm(group,'Can change user'),
           'addrole':urlRequest.user.has_group_perm(group,'Can add gus_role'),
           'delrole':urlRequest.user.has_group_perm(group,'Can delete gus_role'),
           'editrole':urlRequest.user.has_group_perm(group,'Can change gus_role'),
              }
    return render_to_response('groups/viewGroup.html',
        { 'group':group, 'role':role,'roles':roles,'can':my_perms,
          'formAddUser':form_addUser},
          context_instance=RequestContext(urlRequest)
          )
@login_required
def deleteGroup(urlRequest, group_id):
    group = gus_group.objects.get(pk=group_id)
    try:
        if urlRequest.POST['confirm']:
            group.delete()

            return HttpResponseRedirect('/groups/')
    except:
        return render_to_response('generic/confirm_delete.html',
                              {'type' : 'group',
                               'item' : group.group_name,
                               'cancel_url' : '/groups/%s/Edit'%group_id},
                              context_instance = RequestContext(urlRequest))

