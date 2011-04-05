from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from smtplib import SMTPException

from gus_emailer.models import Emailer
from gus_users.models import gus_user
from gus_groups.utils import *
from gus_roles.models import gus_role
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    recipients = forms.EmailField()
    bcc_myself = forms.BooleanField(required=False)
    
    def add_emails(self, inuser):
        # build a list of people to send to
        # get a list of groups and users from them
        groups = getGroupsWithUser(inuser)
        # get users from those groups
        users_list = [(group, gus_role.objects.users_with_group(group)) for group in groups]
        for group, users in users_list:
            us = []
            for user in users:
                em = user.getEmail()
                us.append((em, '%s %s (%s) [%s]' % (user.username,
                                               user.get_full_name(),
                                               em,
                                               user.group_role(group)._role_name)))
            
            # add a section for each group the user is a part of
            self.fields['to_email %s' % group] = \
                forms.BooleanField(
                    widget=forms.CheckboxSelectMultiple(choices=us),
                    label=group.group_name)
    
def check(request, pagenum=1):
    # if we are an anonymous user, redirect to login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    
    # numberify pagenum - this will never fail due to the regex
    pagenum = int(pagenum)
        
    # fetch snippets
    em = Emailer(request.user)
    snippets = em.check_email()
    
    # paginate the emails
    snippets_per_page = 50
    paginator = Paginator(snippets, snippets_per_page)
    
    # default to last page if page number is invalid (too high)
    try:
        page = paginator.page(pagenum)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    
    return render_to_response('email/check.html',
                              {'username':request.user.username,
                               'useremail':request.user.getEmail(),
                               'page': page,
                               },
                              context_instance=RequestContext(request))
    
def check_message(request, uid):
    # if we are an anonymous user, redirect to login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
        
    em = Emailer(request.user)
    message = em.check_message(uid)
    
    # display error message, if applicable
    if type(message) == type((True, '')):
        return render_to_response('email/error.html',
                          {'error_message': message[1],
                           'refresh': message[0]
                           },
                          context_instance=RequestContext(request))
    
    
    
    return render_to_response('email/check_message.html',
                          {'email': message
                           },
                          context_instance=RequestContext(request))
        
def send(request, user_ids=[]):
    # check if we are sending to a user
    if len(user_ids) > 0:
        try:
            usrs = [gus_user.objects.get(pk=user_id).email for id in user_ids]
        except:
            return HttpResponseRedirect('/login/')

    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            
            # if we are an anonymous user, ask to log in
            if not request.user.is_authenticated():
                return HttpResponseRedirect('/login/')
                
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
        if len(user_ids) > 0:
            form = ContactForm({'recipients':', '.join(usrs)})
        else:
            form = ContactForm() # An unbound form
    
    form.add_emails(request.user)

    return render_to_response('email/index.html', {
        'email_form': form, 
    }, context_instance=RequestContext(request))

