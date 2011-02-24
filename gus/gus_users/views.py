from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from gus_roles.models import gus_role
from gus_users.models import gus_user

class loginForm(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

def index(request):
    return HttpResponse('Hello World')

def login(request):    

    if request.method == 'POST': # If the form has been submitted...
        form = loginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/')
        return render_to_response("users/login.html",{"form":form},context_instance=RequestContext(request))
    else:
        form = loginForm()

    return render_to_response("users/login.html",{"form":form},context_instance=RequestContext(request))
    
def register(request):    
    return render_to_response("users/register.html")


def users_groups(request):
    usr=gus_user.objects.get(pk=1)
    my_roles=gus_role.objects.with_user(usr)
    return render_to_response('users/grouplisting.html', {'roles':my_roles})


