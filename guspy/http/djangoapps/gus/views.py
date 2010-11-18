from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from django import forms

class ContactForm(forms.Form):
    real_name = forms.CharField(max_length=100)
    requested_user_name = forms.CharField(max_length=100)
    user_password =  forms.CharField( widget=forms.PasswordInput, label="Your Password" )
    shell_access = forms.BooleanField(required=False)
    user_mail=forms.EmailField(label="Your REAL email")


def index_not_logged(request,args):
	return render_to_response('home_nologin.html')

#def contact_joran(request):
#	form=ContactForm()
#	return render_to_response('contact_joran.html',{'form':form},context_instance=RequestContext(request))

def contact_joran(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
	    from django.core.mail import send_mail
	    msg =  "Add User : "+form.cleaned_data['real_name']+" <"+form.cleaned_data['user_mail']+">\r\n"
	    msg += "Requested username:'"+form.cleaned_data['requested_user_name']+"'    Pass:'"+form.cleaned_data['user_password']+"'\r\n";
	    if(form.cleaned_data['shell_access']):
		msg += "Add To SHELL : YES\r\n"
	    else:
		msg += "Do NOT add to shell\r\n"

            send_mail('Gus Member Request', msg,form.cleaned_data['user_mail'],['joranbeasley+gusmem@gmail.com'], fail_silently=False)

            # Process the data in form.cleaned_data
            # ...
            return HttpResponse('thanks, this just got mailed to joran, hes usually pretty quick about adding users, however he may take upto 24 hrs to respond.') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render_to_response('contact_joran.html', {
        'form': form,
    },context_instance=RequestContext(request))

