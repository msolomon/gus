from django.shortcuts import render_to_response
from django.http import HttpResponse ,HttpResponseRedirect
from django import forms
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from gus_roles.models import gus_role
from gus_users.models import gus_user
from django.contrib.auth import authenticate,login
from django.contrib.auth.views import logout_then_login

class loginForm(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

def index(request):
    return HttpResponse('Hello World')

def logoutView(request):
    return logout_then_login(request,'/login/')
    
def loginView(request):    

    if request.method == 'POST': # If the form has been submitted...
        form = loginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            un=form.cleaned_data['user']
            pw=form.cleaned_data['password']
            user = authenticate(username=un,
                                password=pw)
            if(user):
                login(request, user)
                return HttpResponseRedirect('/gus_test/User/Auth_Test/')
    else:
        form = loginForm()

    return render_to_response("users/login.html",{"form":form},context_instance=RequestContext(request))
    
def register(request):    
    return render_to_response("users/register.html")


def users_groups(urlRequest,user_id):
    try:
        usr = gus_user.objects.get(pk=user_id)
    except:
        return HttpResponse("This User Does not exist<br/>")
    my_roles=gus_role.objects.with_user(usr)
    return render_to_response('users/grouplisting.html', {'roles':my_roles}, context_instance=RequestContext(urlRequest))
