from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from smtplib import SMTPException

from gus_emailer.models import Emailer
from gus_users.models import gus_user
from gus_groups.utils import *
from gus_roles.models import gus_role
from gus_groups.models import gus_group
from django import forms

class SendForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    recipients = forms.CharField(max_length=1000, required=False)
    
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
                forms.CharField(max_length=1000,
                    widget=forms.CheckboxSelectMultiple(choices=us),
                    label=group.group_name,
                    required=False)
                
@login_required
def check(request, pagenum=1):
    # numberify pagenum - this will never fail due to the regex
    pagenum = int(pagenum)
        
    # fetch snippets
    em = Emailer(request.user)
    snippets = em.check_email()
    
    # paginate the emails
    snippets_per_page = 10
    paginator = Paginator(snippets, snippets_per_page)
    
    # default to last page if page number is invalid (too high)
    try:
        page = paginator.page(pagenum)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    
    return render_to_response('email/check.html',
                              {'username':request.user.get_full_name(),
                               'useremail':request.user.getEmail(),
                               'page': page,
                               },
                              context_instance=RequestContext(request))
    
@login_required
def check_sent(request, pagenum=1):
    # numberify pagenum - this will never fail due to the regex
    pagenum = int(pagenum)
        
    # fetch snippets
    em = Emailer(request.user)
    snippets = em.check_sent_email()
    
    # paginate the emails
    snippets_per_page = 10
    paginator = Paginator(snippets, snippets_per_page)
    
    # default to last page if page number is invalid (too high)
    try:
        page = paginator.page(pagenum)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    
    return render_to_response('email/check_sent.html',
                              {'username':request.user.username,
                               'useremail':request.user.getEmail(),
                               'page': page,
                               },
                              context_instance=RequestContext(request))

@login_required
def check_message(request, uid):        
    em = Emailer(request.user)
    message = em.check_message(uid)
    
    # if we are POSTing, we are deleting
    if request.method == 'POST':
        success = em.delete_message(uid)
        if not success:
            return render_to_response('email/error.html',
                  {'error_message': 'The message could not be deleted.',
                   'refresh': False
                   },
                   context_instance=RequestContext(request))
        return HttpResponseRedirect('/email/check/')
            
    
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

@login_required
def send_group(request, groupid):
    # TODO: make this a little more user friendly
    try:
        group = gus_group.objects.get(id=groupid)
        memids = [str(u.id) for u in gus_role.objects.users_with_group(group)]
        return HttpResponseRedirect('/email/send/%s' % (','.join(memids)))
    except:
        return HttpResponseRedirect('/email/send/')

@login_required
def send(request, user_ids):
    # check if we are sending to users
    if request.method == 'GET':
        usrs = user_ids.split(',')
        if len(user_ids) > 0:
            try:
                usrs = ['"%s" %s' %(u.get_full_name(), u.getEmail())
                         for u in gus_user.objects.filter(pk__in=usrs)]
            except: pass

    if request.method == 'POST': # If the form has been submitted...

        form = SendForm(request.POST) # A form bound to the POST data
        form.add_emails(request.user)
        if form.is_valid(): # All validation rules pass
                
            email = form.cleaned_data
            # add recipient if box checked
            for key in email.keys():
                if key.startswith('to_email '):
                    if len(email[key].strip()) == 0: continue
                    for address in eval(email[key]):
                        email['recipients'] += ' %s' % address

            em = Emailer(request.user)
            try:
                em.send_message(email['subject'],
                                email['message'],
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
            form = SendForm({'recipients':', '.join(usrs)})
        else:
            form = SendForm() # An unbound form
    
    form.add_emails(request.user)

    return render_to_response('email/send.html', {
        'email_form': form, 
    }, context_instance=RequestContext(request))

