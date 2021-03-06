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
from django import forms

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
    return render_to_response('groups/index.html', data
         #'urls':{'delete':'/gus_test/Group/Delete/%s/'},
         ,context_instance=RequestContext(urlRequest));

                                 
@login_required
def addGroup(urlRequest):
    import random
    from gus.gus_groups.utils import createNewGroup
    
    #setup our form
    if urlRequest.method == 'POST': # If the form has been submitted...
        form = SimpleGroupAddForm(urlRequest.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            grp=createNewGroup(
                    form.cleaned_data['group_owner'],
                    form.cleaned_data['group_name'],
                    form.cleaned_data['group_description'],
                    ""
                    )
            if urlRequest.user.is_site_admin():
                grp.group_activated=1
                grp.save()
            return HttpResponseRedirect('/profile/') # Redirect after POST
    else:
        form = SimpleGroupAddForm({'group_owner':urlRequest.user}) # An unbound form
    if not urlRequest.user.is_site_admin():
        form.fields['group_owner'].widget=forms.Select(attrs={'style':'display:none'})
        form.fields['group_owner'].label = "Owner : %s"%urlRequest.user.username
        form.fields['group_owner'].queryset=gus_user.objects.filter(_user=urlRequest.user._user)
    return render_to_response('test/form.html',
                                {
                                 'submiturl':'/groups/Add/',
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
def editGroupDesc(urlRequest, group_id):
    try:
        grp=gus_group.objects.get(id=group_id)
    except:
        return HttpResponseRedirect('/profile/')
    if not urlRequest.user.has_group_perm(grp,'Can change gus_group'):
        return HttpResponseRedirect('/groups/%s/'%group_id)
    class DescEditForm(forms.Form):
        group_description=forms.CharField(widget=forms.Textarea())
        group_id=forms.IntegerField(widget=forms.HiddenInput())
    if urlRequest.method == 'POST':
        form = DescEditForm(urlRequest.POST)
        if form.is_valid():
            grp.group_description = form.cleaned_data['group_description']
            grp.save()
            return HttpResponseRedirect('/groups/%s/'%group_id)
    else:
        form=DescEditForm({'group_id':grp.id,'group_description':grp.group_description})
        return render_to_response('generic/form.html',
                                {'cancelurl':'/groups/%s/'%group_id,
                                 'submiturl':'/groups/%s/Edit/'%group_id,
                                 'enctype':'multipart/form-data',
                                 'form':form,
                                 'title':'Edit Description for %s'%grp.group_name,
                                 'btnlabel':'Save Edits',
                                },
                                context_instance=RequestContext(urlRequest)

                                )
       
@login_required
def requestMembership(urlRequest,group_id):
    """
    Allow user to request membership to a given group
    """
    from gus_roles.models import gus_role
    try:
        group=gus_group.objects.get(id=group_id)
    except:
        return HttpResponseRedirect('/groups/%s/'%group_id)
    if gus_role.objects.with_user_in_group(group, urlRequest.user):
        return HttpResponseRedirect('/groups/%s/'%group_id)
    group.pending_users.add(urlRequest.user)
    return HttpResponseRedirect('/groups/%s/'%group_id)

def viewGroup(urlRequest, group_id):
    from gus.gusTestSuite.forms import SimpleAddUserToGroup
    if group_id == 2 and not urlRequest.user.is_site_admin():
        return HttpResponseRedirect('/profile/')
    if urlRequest.method == 'POST':
        usr = gus_user.objects.get(pk=int(urlRequest.POST['new_member']))
        role = gus_role.objects.get(pk=int(urlRequest.POST['role']))
        role.users.add(usr)
    group = gus_group.objects.get(pk=group_id)
    form_addUser = SimpleAddUserToGroup(group)
    role=gus_role.objects.with_user_in_group(group,urlRequest.user)
    roles = group.roles
    tmp_users_list= gus_role.objects.users_without_group(group)
    users_tmp_namelist = [usr.username for usr in tmp_users_list]
    userstr ='"'+ '","'.join(users_tmp_namelist) +'"'
    isSubGrouped=False
    if not role and not urlRequest.user.is_anonymous():
        isSubGrouped = urlRequest.user.has_subgroup_membership(group)
        
    #return HttpResponse(userstr)
    if urlRequest.user.is_authenticated():
        my_perms={
           'adduser':urlRequest.user.has_group_perm(group,'Can add gus_user'),
           'deluser':urlRequest.user.has_group_perm(group,'Can delete gus_user'),
           'edituser':urlRequest.user.has_group_perm(group,'Can change gus_user'),
           'addrole':urlRequest.user.has_group_perm(group,'Can add gus_role'),
           'delrole':urlRequest.user.has_group_perm(group,'Can delete gus_role'),
           'editrole':urlRequest.user.has_group_perm(group,'Can change gus_role'),
           'editgroup':urlRequest.user.has_group_perm(group,'Can change gus_group'),
           'addgroup':urlRequest.user.has_group_perm(group,'Can add gus_group'),
           'delgroup':urlRequest.user.has_group_perm(group,'Can delete gus_group'),
        }
    else:
        # no permissions for anonymous users
        my_perms = {
                    'adduser': False,
                    'deluser': False,
                    'edituser': False,
                    'addrole': False,
                    'delrole': False,
                    'editrole': False,
                    'editgroup': False,
                    'addgroup': False,
                    'delgroup': False
                    }
    return render_to_response('groups/viewGroup.html',
        { 'group':group, 'role':role,'roles':roles,'can':my_perms,
          'formAddUser':form_addUser,'addUserString':userstr},
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
                               'cancel_url' : '/groups/%s/'%group_id},
                              context_instance = RequestContext(urlRequest))

@login_required
def AddSubgroup(urlRequest,group_id):

    try:
        group=gus_group.objects.get(pk=group_id)
        #ensure that we can add groups
        if not urlRequest.user.has_group_perm(group,'Can add gus_group'):
            return HttpResponseRedirect('/groups/%s/'%group_id)
    except:
        return HttpResponseRedirect('/')
    if urlRequest.method == 'POST':
        form = SimpleSubGroupAddForm(urlRequest.POST)
        if form.is_valid():
            try:
                grp = gus_group.objects.create_group(form.cleaned_data['group_name'],form.cleaned_data['group_description'],form.cleaned_data['group_image'] or "")
                grp.parent_group=group
                grp.group_activated=1
                grp.save()
            except:
                pass
            return HttpResponseRedirect('/groups/%s/'%group_id)
    else:
        form = SimpleSubGroupAddForm({'parent_group':group_id})

    return render_to_response('test/form.html',
                                {
                                 'submiturl':'/groups/%s/Addsubgroup/'%group_id,
                                 'enctype':'multipart/form-data',
                                 'form':form,
                                 'title':'Add Subgroup to %s'%group.group_name,
                                 'btnlabel':'Create Subgroup',
                                },
                                context_instance=RequestContext(urlRequest)

                                )

@login_required
def removeUserFromRole(urlRequest, user_id, role_id):
    user = gus_user.objects.get(pk=user_id)
    role = gus_role.objects.get(pk=role_id)
    g_id = role.group.id
    role.users.remove(user)
    return HttpResponseRedirect('/groups/%s/'%g_id)

@login_required
def removeUserFromGroup(urlRequest, group_id, user_id):
    group = gus_group.objects.get(pk=group_id)
    user = gus_user.objects.get(pk=user_id)
    r = gus_role.objects.with_user_in_group(group,user)
    return removeUserFromRole(urlRequest, user_id, r.id)

@login_required
def deleteRole(urlRequest, role_id):
    role = gus_role.objects.get(pk=role_id)
    g_id = role.group.id
    role.delete()
    return HttpResponseRedirect('/groups/%s/'%g_id)


@login_required
def editRole(urlRequest, group_id, user_id):
    try:
        group = gus_group.objects.get(pk=group_id)
        usr = gus_user.objects.get(pk=user_id)
    except:
        return HttpResponseRedirect('/groups/%s/'%group_id)

    role = gus_role.objects.with_user_in_group(group, usr)

    try:
        if urlRequest.POST['newRole']:
            r2 = gus_role.objects.get(pk=int(urlRequest.POST['newRole']))
            role.users.remove(usr)
            r2.users.add(usr)
            return HttpResponseRedirect("/groups/%s/"%group_id)
    except:
        return render_to_response('groups/manageRole.html',
                       {
                         'role':role, 'usr':usr, 'group':group

                       },context_instance=RequestContext(urlRequest)
                       )
@login_required
def editRolePerms(urlRequest,role_id):
    role = gus_role.objects.get(pk=role_id)
    if urlRequest.method == 'POST':
        form = RolePermissionForm(urlRequest.POST)
        if form.is_valid():
            role._role_permissions.permissions.clear()
            role._role_permission_level = int(form.cleaned_data['is_superUser'])
            [role._role_permissions.permissions.add(r) for r in form.cleaned_data['role_permissions']]
            role.save()
            g_id = role.group.id
            return HttpResponseRedirect("/groups/%s/"%g_id)
    else:
        if role._role_permission_level >= 1:
            is_superUser = True
        else:
            is_superUser = False
        role_permissions = role._role_permissions.permissions.all()
        data = {'id':role_id, 'is_superUser':is_superUser, 'role_permissions':role_permissions}
        form = RolePermissionForm(data)

    #return HttpResponse("WIP")

    return render_to_response('test/form.html',
                                {
                                 'submiturl':('/groups/EditPerms/%s/'%role_id),
                                 'encType':'multipart/form-data',
                                 'form':form,
                                 'title':'Edit Permissions For Role %s'%role.name,
                                 'btnlabel':'Save Role',
                                },
                                context_instance=RequestContext(urlRequest)
                              )
@login_required
def createRole(urlRequest,group_id):
    group = gus_group.objects.get(pk=group_id)
    if urlRequest.method == 'POST':
        form = RoleCreateForm(urlRequest.POST)
        if form.is_valid():
            role = gus_role.objects.create_role(group,form.cleaned_data['role_name'])
            if form.cleaned_data['is_superUser'] == True:
                role._role_permission_level = 1
            [role._role_permissions.permissions.add(r) for r in form.cleaned_data['role_permissions']]
            role.save()
            return HttpResponseRedirect("/groups/%s/"%group_id)
    else:
        form = RoleCreateForm({'id':group_id})
        
#    return HttpResponse("WIP")
    return render_to_response('test/form.html',
                                {
                                 'submiturl':('/groups/%s/CreateRole/'%group_id),
                                 'encType':'multipart/form-data',
                                 'form':form,
                                 'title':'Create Role for %s'%group.group_name,
                                 'btnlabel':'Create Role',
                                },
                                context_instance=RequestContext(urlRequest)
                              )

@login_required
def ApproveGroup(urlRequest):
    if not urlRequest.user.is_site_admin():
        return HttpResponseRedirect('/profile/')
    if urlRequest.method == 'POST':
        form = ApprovalForm(urlRequest.POST)
        if form.is_valid():
            try:
                grp=gus_group.objects.get(id=int(form.cleaned_data['group_id']))
                grp.group_activated=int(form.cleaned_data['is_active'])
                grp.save()
            except:
                pass
            
            return  HttpResponseRedirect('/groups/ApproveGroup/')
    groups = gus_group.objects.filter(group_activated=0)
    g2 = [{'group':g,'form':ApprovalForm({'group_id':g.id})} for g in groups]
    return render_to_response('groups/unapproved.html',
                              {'groups':g2,
                               },
                              context_instance=RequestContext(urlRequest))

@login_required
def ApproveUser(urlRequest,group_id):
    try:
        group = gus_group.objects.get(id=group_id)
        
    except:
        return HttpResponseRedirect('/profile/')
    if not urlRequest.user.has_group_perm(group,'Can add gus_user'):
        return HttpResponseRedirect('/groups/%s/'%group_id)
    if urlRequest.method == 'POST':
        
        form = UserApprovalForm(urlRequest.POST)
        
        if form.is_valid():
            from django.contrib.auth.models import User   
            
            try:
                usr=gus_user.objects.get_id(form.cleaned_data['user_id'])
                role=form.cleaned_data['user_role']
                role.users.add(usr)
                role.save()
                
            except:
                
                return HttpResponseRedirect('/')
                
            group.pending_users.remove(usr)
            group.save()
            
            
            return  HttpResponseRedirect('/groups/%s/ApproveUser/'%group_id)
    
    users_tmp=group.pending_users.all()
    users = [{'user':u,'form':UserApprovalForm({'user_id':u.id})} for u in users_tmp]
    for u in users:
        u['form'].fields['user_role'].queryset=gus_role.objects.with_group(group)
    return render_to_response('groups/unapprovedUser.html',
                              {'users':users,
                               },
                              context_instance=RequestContext(urlRequest))
