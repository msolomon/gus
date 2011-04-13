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

