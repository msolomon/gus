# Mike Solomon is to blame for content herein

from imaplib import *
from django.db import models
from django.core import mail
from gus import settings

from gus.gus_widget.models import Widget
from gus.gus_groups.models import gus_group
from gus.gus_users.models import gus_user
from gus.gus_roles.models import gus_role

import sys
sys.path.append('gus_emailer/IMAPClient_0_7/imapclient/')
from imapclient import IMAPClient

class EmailerWidget(Widget):
    '''
    The widget for managing emails within a group.
    '''
    # what else is needed besides the name (provided by Widget)? (perm strings)
    permission_strings="can_send|can_send_group" #maybe? -jb
    def __init__(self):
        self._e = Emailer()

    
class Emailer(models.Model):
    '''
    An email manager for a specific user
    '''
    #user = models.ForeignKey(gus_user)
    myplaintextpassword = models.CharField(max_length=128)
    #myusername = user.name
#    imap_host = models.CharField(max_length=128)
#    imap_port = models.SmallIntegerField()
#    imap_user = models.CharField(max_length=16)
#    imap_password = models.CharField(max_length=16)
    
    def __init__(self, usr):
        self.user = usr
        self.user_email = usr.getEmail()
    
    def sendto_group(self, email):
        ''' Email a message to the whole group.
            @param email: the email object
            @type email: mail.EmailMessage
        '''      
        groups = [x.group() for x in gus_role.objects.with_user(self.user)]
        # list of tuples (group, list of group users)
        ## group_users = [(g, [u for u in gus_role.objects.users_with_group(g)]) for g in groups]
        all_users = [u.getEmail() for u in [gus_role.object.users_with_group(g) for g in groups]]
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
        '''Check for email messages, and return a list of them
            @return: [mail.EmailMessage]
        '''
        
        def parse_rfc822(mes, body):
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
        
        server = IMAPClient(settings.IMAP_HOST, use_uid=False, ssl=True)
        server.login(settings.IMAP_HOST_USER, settings.IMAP_HOST_PASSWORD)
        
        select_info = server.select_folder('INBOX')
        messages = server.search(['NOT DELETED'])
        response = server.fetch(messages, ['FLAGS', 'BODY[HEADER]', 'BODY[TEXT]'])# 'RFC822'
    
        emails = []
        for v in response.values():
            em = parse_rfc822(v['BODY[HEADER]'], v['BODY[TEXT]'])
            # ensure the email was sent to this user.
            # TODO: only query for such emails
            if self.user_email in \
                ' '.join(em.to + em.cc + em.bcc).translate(None, "\"'<>,").split():
                    emails.insert(0, em)
    
        server.logout()
        return emails
