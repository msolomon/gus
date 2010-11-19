from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

class register_form(forms.Form):
	real_name=forms.CharField(max_length=100)
	desired_username=forms.CharField(max_length=100)
	password=forms.CharField(max_length=100,widget=forms.PasswordInput)
	email=forms.CharField(max_length=100)
	enable_shell_access=forms.BooleanField(required=False)
	
class login_form(forms.Form):
	username=forms.CharField(max_length=100)
	password=forms.CharField(widget=forms.PasswordInput,max_length=100)

def index(request,leftovers):
	if request.method == 'POST': # If the form has been submitted...
        	rform = register_form(request.POST) # A form bound to the POST data
        	if rform.is_valid(): # All validation rules pass
            		# Process the data in form.cleaned_data
            		# ...
			from gus.Jauth.models import *
			jp=Jorans_Pending()
			jp.real_name = rform.cleaned_data['real_name']
			jp.email=rform.cleaned_data['email']
			jp.pw=rform.cleaned_data['password']
			jp.desired_user=rform.cleaned_data['desired_username']
			if rform.cleaned_data['enable_shell_access'] : jp.desired_user+="(SHELL ACCESS TOO PLEASE)"
			jp.save()
            		return HttpResponseRedirect('/thanks/') # Redirect after POST
        	lform = login_form(request.POST) # A form bound to the POST data
        	if lform.is_valid(): # All validation rules pass
            		# Process the data in form.cleaned_data
            		# ...
            		return HttpResponseRedirect('/thanks/') # Redirect after POST
     	else:
		rform = register_form()
		lform = login_form()
	import subprocess
	_proc = subprocess.Popen('git log --no-color -n 1 --date=iso',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	try:
    		GIT_REVISION_DATE =[x.split('Date:')[1].split('+')[0].strip() 
		for x in _proc.communicate()[0].splitlines() 
			if x.startswith('Date:')][0]
	except IndexError:
    		GIT_REVISION_DATE = 'unknown'

    	return 
render_to_response('index_joran.html',{'lform':lform,'rform':rform,'revision':GIT_REVISION_DATE},context_instance=RequestContext(request))
	
def thanks(request):
	return render_to_response('feedback_recieved.html',{'msg':'Please Wait For Approval'})


