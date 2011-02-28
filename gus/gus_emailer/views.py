from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.forms import ModelForm
from smtplib import SMTPException

from gus_emailer.models import EmailerWidget, Emailer
from django import forms

#class ContactForm(ModelForm):
#    def __init__(self, usr):
#        self.usr = usr
#    class Meta:
#        def __init__(self):
#            model = Emailer(self.usr)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    recipients = forms.EmailField()
    bcc_myself = forms.BooleanField(required=False)
    
def index(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            
            # if we are an anonymous user, send from test account
            # TODO: remove this once user authentication system is complete
            if not request.user.is_authenticated():
                request.user.getEmail = lambda: 'guspyuser@gmail.com'
                
            email = form.cleaned_data
            # add sender to recipients if box checked
            if email['bcc_myself']:
                email['recipients'] += ' %s' % request.user.getEmail()
                
            em = Emailer(request.user)
            try:
                em.send_message(email['subject'],
                                email['message'],
                                # TODO: sanitize email recipient list
                                email['recipients'].split()
                                )
            except SMTPException, e:
                email['message_send_failed'] = e
                email['success'] = False
            else:
                email['success'] = True

            return render_to_response('email/sent.html', {'email': email},
                                      context_instance=RequestContext(request))
    else:
        form = ContactForm() # An unbound form

    return render_to_response('email/index.html', {
        'email_form': form, 
    }, context_instance=RequestContext(request))
    