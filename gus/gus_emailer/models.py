# Mike Solomon is to blame for content herein

import email, re

from imaplib import *
from django.db import models
from django.core import mail
from gus import settings

from gus.gus_widget.models import Widget
from gus.gus_groups.models import gus_group
from gus.gus_users.models import gus_user
from gus.gus_roles.models import gus_role

import sys
sys.path.append('gus_emailer/libs/IMAPClient_0_7/imapclient/')
sys.path.append('gus_emailer/libs/python-dateutil-1_5/')
from imapclient import IMAPClient
from dateutil.parser import parse

class EmailerWidget(Widget):
    '''
    The widget for managing emails within a group.
    '''
    def __init__(self):
        self._e = Emailer()
    
class Emailer(models.Model):
    '''
    An email manager for a specific user
    '''
    #user = models.ForeignKey(gus_user)
    #myplaintextpassword = models.CharField(max_length=128)
    #myusername = user.name
#    imap_host = models.CharField(max_length=128)
#    imap_port = models.SmallIntegerField()
#    imap_user = models.CharField(max_length=16)
#    imap_password = models.CharField(max_length=16)
    
    def __init__(self, usr):
        self.user = usr
        self.user_email = usr.getEmail()
    
    def sendto_group(self, email, group):
        ''' Email a message to the whole group.
            @param email: the email object
            @param group: the group object
            @type email: mail.EmailMessage
        '''      
        #groups = [x.group for x in gus_role.objects.with_user(self.user)]
        emails = [u.getEmail() for u in gus_role.objects.users_with_group(group)] 
#        all_users = [u.getEmail() for sublist in 
#                        [gus_role.objects.users_with_group(g) for g in groups]
#                        for u in sublist]
        email.bcc.extend(emails)
        email.send()

    def send_message(self, subject, message, recipient_list, connection=None):
        ''' Send an email to a list of recipients
            @param subject: the email subject
            @type subject: string
            @param message: email body
            @param message: string
            @param recipient_list: a list of email address strings
            @type recipient_list: [string]
            @param connection: an email backend connection
            @type connection: mail.backends.base
        '''
        mail.send_mail(subject, message, self.user.getEmail(),
                   recipient_list, connection=connection)

    def set_imap(self, host, port):
        ''' Set the imap host and port
            @param host: imap host
            @type host: string
            @param port: imap port
            @type port: integer
        '''
        self.imap_host = host #models.CharField(host)
        self.imap_port = port #models.SmallIntegerField(port)
    
    def set_imap_user(self, user, password):
        ''' Set the imap username and password
            @param user: imap username
            @type user: string
            @param password: imap password
            @type password: string
        '''
        self.imap_user = user #models.CharField(user)
        self.imap_password = password #models.CharField(password)
    
    def check_email(self):
        '''Check for email messages, and return a list of snippets
            @return: [{uid, subject, from, date}...]
        '''

        server = IMAPClient(settings.IMAP_HOST, use_uid=False, ssl=True)
        server.login(settings.IMAP_HOST_USER, settings.IMAP_HOST_PASSWORD)
        
        select_info = server.select_folder('INBOX')
        
        # get a list of messages prefiltered for this user
        potentials = server.search([' NOT DELETED',
                                  'TO ' + self.user_email])
        potentials += server.search([' NOT DELETED',
                                  'CC ' + self.user_email])
        response = server.fetch(potentials, ['BODY.PEEK[HEADER]'])
        server.logout()
        
        # perform more robust filtering of returned messages
        snippets = []
        for id, message in response.iteritems():
            mes = message['BODY[HEADER]']
            try:
                to = re.search('to:([^\n]*)\n', mes, re.IGNORECASE).group(1).strip()
            except IndexError: continue
            
            # create the snippets
            if self.user_email in to.translate(None, '\'"<>').split():
                try:
                    date = re.search('date:([^\n]*)\n', mes, re.I).group(1).strip()
                    date = parse(date).strftime('%I:%M %p, %x')
                except (IndexError, ValueError, TypeError): date = ''
                try: frm = re.search('from:([^\n]*)\n', mes, re.I).group(1).strip()
                except IndexError:  frm = ''    
                try:  sub = re.search('subject:([^\n]*)\n', mes, re.I).group(1).strip()
                except IndexError: sub = ''   
                    
                snippets.insert(0, {'id': id,
                                    'subject': sub,
                                    'from': frm,
                                    'date': date
                                    })      
            
        return snippets
    
    def check_message(self, emailuid):
        '''Check for a specified email message and return it
            @param int, the email UID to get
            @return: mail.EmailMessage
        '''
        notfound = 'This email message could not be found, ' + \
                   ' or you do not have the rights to view it.'
        server = IMAPClient(settings.IMAP_HOST, use_uid=False, ssl=True)
        server.login(settings.IMAP_HOST_USER, settings.IMAP_HOST_PASSWORD)
        
        select_info = server.select_folder('INBOX')
        
        # get a list of messages prefiltered for this user
        potential = server.search(['UID ' + emailuid])
        if len(potential) == 0:
            return (False, notfound)
        
        # otherwise, get the message and log out
        messages = server.fetch(potential, ['BODY[HEADER]', 'BODY[TEXT]'])
        server.logout()
        
        # ensure there is exactly one message
        if len(messages) != 1:
            return (False, notfound)
        
        # extract the message and put it into an EmailMessage object
        k = messages.keys()[0]
        try:
            message = self.parse_rfc822(messages[k]['BODY[HEADER]'],
                                        messages[k]['BODY[TEXT]'])
        except KeyError:
            return (True, 'The email message could not be retrieved. Retrying...')
        
        # ensure the logged-in user was sent this email
        dest = ' '.join(message.to + message.cc + message.bcc)
        dest = dest.split()
        
        if self.user_email not in dest:
            return (False, notfound)
    
        return message 
    
    def parse_rfc822(self, mes, body):
        ''' Parse a message in RFC822 format, split into header and body.
            @param mes: the header in RFC822 format
            @param body: the body (plain text)
            @return: EmailMessage object
        '''
        ## TODO: Account for things like multiple recipients
                ##     and, say, including other header info
        m = mes.split('\n')
        ## Get header fields
        def getrest(prefix):
            for line in m:
                if line.startswith(prefix):
                    return line[len(prefix):].strip()
                
        subject = getrest('Subject: ')
        from_email = getrest('From: ')
        to = getrest('To: ')

        return mail.EmailMessage(
                    subject,
                    body,
                    from_email,
                    [to],
                    None)        
        