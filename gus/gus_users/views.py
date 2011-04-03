from django.shortcuts import render_to_response
from django.http import HttpResponse ,HttpResponseRedirect
from django import forms
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from gus_roles.models import gus_role
from gus_users.models import gus_user
from gus_groups.models import gus_group
from gus_bill.models import bill
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



#group_id will be used for our profile page
# beginnings of profile view that Chandler and Nathan are working on
def profile(urlRequest):
    my_self = urlRequest.user
    my_roles = gus_role.objects.with_user(my_self)
    return render_to_response('users/profile.html', {'roles':my_roles, 'usr':my_self}, context_instance=RequestContext(urlRequest))
    
    
# Note to self: This function uncovered a naming inconsistency;
#    the group name is group_name, the user name is username, and the role name is just "name"
#    Bring up at next meeting
def profile_sub(urlRequest, group_id):
    my_self = urlRequest.user
    my_group = gus_group.objects.get(pk=group_id)
    my_role = gus_role.objects.with_user_in_group(my_group, my_self)
    my_bill = bill.objects.filter(user = my_self.id)
    #with_user_in_group(my_group, my_self)
    return render_to_response('users/profilesub.html', {'usr':my_self, 'grp':my_group, 'role':my_role, 'bill':my_bill}, context_instance=RequestContext(urlRequest))



def users_groups(urlRequest,user_id):
    try:
        usr = gus_user.objects.get(pk=user_id)
    except:
        return HttpResponse("This User Does not exist<br/>")
    my_roles=gus_role.objects.with_user(usr)
    # Note to self: always include that last argument "context_instance=RequestContext(urlRequest)"
    return render_to_response('users/grouplisting.html', {'roles':my_roles}, context_instance=RequestContext(urlRequest))
