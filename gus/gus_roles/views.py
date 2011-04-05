###################################################
#####   Currently unused .... maybe delete?    ####
###################################################

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from  django.template import RequestContext

from gus_roles.models import *
from django import forms
"""
--this was just practice view code for lee

class add_form(forms.Form):
    new_member = forms.ModelMultipleChoiceField(
                            queryset=[]
                            )
    def __init__(self, role, data=None):
        super(add_form, self).__init__(data)
        self.fields[
            'new_member'
            ].queryset = gus_role.objects.users_without_role(role)
	

def index(request):
    role = gus_role.objects.all()[0]
    return render_to_response('roles/index.html', {'role': role})

def add_user_to_role(request, role_id):
    role = gus_role.objects.get(pk=role_id)
    if request.method == 'POST': # If the form has been submitted..
	form = add_form(role,request.POST)
	form.is_valid()
	return HttpResponse(form.errors)#['users'])
	#return HttpResponse('form not valid')

    form = add_form(role)
	
    users = gus_role.objects.users_without_role(role)
    return render_to_response('roles/add_user.html', {'users_list': users, 'role': role, 'form': form}, context_instance=RequestContext(request))
"""

def index(request):
    role = gus_role.objects.all()[0]
    return render_to_response('roles/index.html', {'role': role})


def removeUserFromRole(urlRequest, user_id, role_id):
    user = gus_user.objects.get(pk=user_id)
    role = gus_role.objects.get(pk=role_id)
    role.users.remove(user)
    return HttpResponseRedirect('/gus_test/Role/Edit/%s'%role_id)
def editRole(urlRequest, role_id):

    role = gus_role.objects.get(pk=role_id)



    return render_to_response('groups/manageRole.html',
                       {
                         'role':role,

                       },context_instance=RequestContext(urlRequest)
                       )

def createRole(urlRequest,group_id):
    group = gus_group.objects.get(pk=group_id)
    if urlRequest.method == 'POST':
        form = RoleCreateForm(urlRequest.POST)
        if form.is_valid():
            role = gus_role.objects.create_role(group,form.cleaned_data['role_name'])
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
            [role._role_permissions.permissions.add(r) for r in form.cleaned_data['role_permissions']]
    else:
        role_permissions = role._role_permissions.permissions.all()
        data = {'id':role_id, 'role_permissions':role_permissions}
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
                                 
