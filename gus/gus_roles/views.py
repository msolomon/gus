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