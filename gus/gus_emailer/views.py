from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from  django.template import RequestContext

from gus_emailer.models import EmailerWidget
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    recipients = forms.EmailField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    
def index(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            
            message = form.cleaned_data['message']
            return HttpResponseRedirect('thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render_to_response('email/index.html', {
        'email_form': form, 
    }, context_instance=RequestContext(request))
    
