# Mike Solomon is to blame for content herein

import email, re

from imaplib import *
from django.db import models
from django.core import mail
from gus import settings
import datetime, logging, hashlib

from django.contrib.auth.models import User
from gus.gus_widget.models import Widget
from gus.gus_groups.models import gus_group
from gus.gus_users.models import gus_user
from gus.gus_roles.models import gus_role
from django.utils.encoding import smart_str
import bleach

import sys, os
sys.path.append(os.path.join(settings.PROJECT_PATH,
                             'gus_emailer/libs/IMAPClient_0_7/imapclient/'))
sys.path.append(os.path.join(settings.PROJECT_PATH,
                             'gus_emailer/libs/python-dateutil-1_5/'))

from imapclient import IMAPClient
from dateutil.parser import parse

def rm_illegal(string):
    return ''.join([l for l in string if l not in '\'"<>,'])

class EmailerWidget(Widget):
    '''
    The widget for managing emails within a group.
    '''
    def __init__(self):
        self._e = Emailer()
        
class DBEmail(models.Model):
    '''
    An actual email stored in the database
    '''

    date = models.DateTimeField(null=True, blank=True)
    header = models.TextField()
    body = models.TextField()
    sender = models.CharField(max_length=100)
    recipients = models.CharField(max_length=1000)
    hash = models.CharField(max_length=130)
    gus_receivers = models.ManyToManyField(gus_user)
    gus_sender = models.ForeignKey(gus_user, null=True, blank=True,
                                      related_name='gus_user.dbemail.gus_sender')
    deleted = models.ManyToManyField(gus_user, related_name='gus_user.dbemail.deleted')
    viewed = models.ManyToManyField(gus_user, related_name='gus_user.dbemail.viewed')
    
    
    def fill(self, header, body, date, sender, recipients, gus_recipients):
        h = hashlib.md5()
        h.update(smart_str(body))
        try:
            h.update(date.ctime())
        except Exception, e:
            logging.debug(e)
        h.update(smart_str(sender))
        h.update(smart_str(recipients))
        h.update(smart_str(gus_recipients))
        self.hash = h.hexdigest()
        try:
            #print 'fill'
            DBEmail.objects.get(hash=self.hash)
        except Exception, e:
            logging.debug(e)
            #print 'unique', hash
            self.header = header
            self.body = body
            self.date = date
            self.sender = sender
            if sender.endswith(settings.EMAIL_SUFFIX):
                try:
                    self.gus_sender = gus_user.objects.get(_user=User.objects.get(
                                username__iexact=sender[:-len(settings.EMAIL_SUFFIX)]))
                except: pass
            self.recipients = recipients
            self.save() # to establish primary key
            for r in gus_recipients:
                try:
                    self.gus_receivers.add(
                        gus_user.objects.get(
                            _user=User.objects.get(username__iexact=r)
                            )
                        )
                except Exception, e:
                    logging.debug(e)
            self.save(force_update=True)
            return
        # if we got here, this message was not unique
        #print 'deleting', hash
        #self.delete()
    
    def delete_email(self, user):
        self.deleted.add(user)
    
    def view(self, user):
        self.viewed.add(user)
    
class Emailer():
    '''
    An email manager for a specific user
    '''
    
    def __init__(self, usr):
        self.user = usr
        self.user_email = usr.getEmail()
    
    def sendto_group(self, email, group):
        ''' Email a message to the whole group.
            @param email: the email object
            @param group: the group object
            @type email: mail.EmailMessage
        '''      
        emails = [u.getEmail() for u in gus_role.objects.users_with_group(group)] 
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
        address = self.user.getEmail()
        mail.send_mail(subject, message, address,
                   recipient_list, connection=connection)
        ## uncomment the lines below to enable sending html. gus will not receive this properly
        #em = mail.EmailMultiAlternatives(subject, message, address,
        #        recipient_list, [], headers={"Reply-To": address})
        #em.attach_alternative(message, 'text/html')
        #em.send()

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
        
    def update_email(self):
        '''
        Fetch email messages from the IMAP server and store them
        @return: None
        '''
        server = IMAPClient(settings.IMAP_HOST, use_uid=False, ssl=True)
        server.login(settings.IMAP_HOST_USER, settings.IMAP_HOST_PASSWORD)
        
        select_info = server.select_folder('INBOX')
        
        # get a list of messages 
        potentials = server.search(['NOT DELETED'])
        response = server.fetch(potentials, ['BODY[HEADER]', 'BODY[TEXT]'])
        
        for k, v in response.iteritems():
            message = self.parse_rfc822(v['BODY[HEADER]'],
                                        v['BODY[TEXT]'])
            # get a list of all recipients
            recip = message.recipients() + message.cc
            # split off gus users from this list for special handling
            gus_recip = []
            for r in recip:
                if r.endswith(settings.EMAIL_SUFFIX):
                    gus_recip.append(r[:-len(settings.EMAIL_SUFFIX)])
            recip = [r for r in recip if r not in gus_recip]
            
            try:
                date = parse(re.search('date:([^\n]*)\n', 
                                 v['BODY[HEADER]'], re.I).group(1).strip())
                t = date.utcoffset()
                date = date.replace(tzinfo=None) - t
            except Exception, e:
                logging.debug(e)
                date = None
            
            # store the email in the DB
            em = DBEmail()
            em.fill(v['BODY[HEADER]'], bleach.clean(v['BODY[TEXT]'], tags=settings.BLEACH_ALLOWED_TAGS), date,
                    message.from_email, recip, gus_recip)
            
            # now delete from server
            server.add_flags(k, ['\Deleted'])
        server.logout()
    
    def check_email(self):
        '''Check for email messages, and return a list of snippets
            @return: [{uid, subject, from, date}...]
        '''
        
        # get new messages
        self.fetch_messages()
        
        messages = DBEmail.objects.filter(gus_receivers=self.user). \
                                    exclude(deleted=self.user).order_by('date')

        snippets = []
        for message in messages:
            mes = message.header

            ## create the snippets
            # parse the date
            try:
                datestr = re.search('date:([^\n]*)\n', mes, re.I).group(1).strip()
                date = parse(datestr)
            except Exception, e:
                logging.debug(e)
                time = datetime.datetime.utcnow().isoformat(' ') + ' -0000'
                date = parse(time)
            t = date.utcoffset()
            date = date.replace(tzinfo=None) - t            
            
            frm, frm_address = self.get_from_with_link(message)
                
            try:  subject = re.search('subject:([^\n]*)\n', mes, re.I).group(1).strip()
            except (IndexError, AttributeError), e:
                logging.debug(e)
                subject = '(no subject)'      
            
            try:
                if message.viewed.filter(dbemail__viewed=self.user):
                    unviewed = False
                else: unviewed = True
            except Exception, e:
                logging.debug(e)
                unviewed = True

            snippets.insert(0, {'id': message.id,
                                'subject': subject,
                                'from': frm,
                                'from_address': frm_address,
                                'date': date.strftime('%I:%M %p, %x'), 
                                'unviewed': unviewed                             
                                })            
        
        return snippets
    
    def fetch_messages(self):
        '''
        Fetch email messages from the IMAP server and store them. This has
        error handling update_email lacks.
        @return: None
        '''
        # double-check email, if fails the first time
        for _ in range(2):
            try: self.update_email()
            except Exception, e:
                logging.debug(e)
                continue
            break

    
    def get_from_with_link(self, message):
        '''
        Return tuples of prettified senders with appropriate links
        @param DBEmail, the email 
        @return: [(link_text, destination), ...]
        '''
        # determine the sender to print
        if message.gus_sender == None:    
            frm = message.sender
            frm_address = 'mailto:%s' % frm
        else:
            frm = '%s (%s)' % (message.gus_sender.get_full_name(), message.gus_sender.username)
            frm_address = '/email/send/%s' % message.gus_sender.pk
        return (frm, frm_address)
    
    def check_sent_email(self):
        '''Check for sent email messages, and return a list of snippets
            @return: [{uid, subject, to, date}...]
        '''
        # double-check email, if fails the first time
        for _ in range(2):
            try: self.update_email()
            except Exception, e:
                logging.debug(e)
                continue
            break

        messages = DBEmail.objects.filter(gus_sender=self.user). \
                                    exclude(deleted=self.user).order_by('date')

        snippets = []
        for message in messages:
            mes = message.header

            ## create the snippets
            
            to_l = self.get_to_with_links(message)
            
            # parse the date
            try:
                datestr = re.search('date:([^\n]*)\n', mes, re.I).group(1).strip()
                date = parse(datestr)
            except Exception, e:
                logging.debug(e)
                time = datetime.datetime.utcnow().isoformat(' ') + ' -0000'
                date = parse(time)
            t = date.utcoffset()
            date = date.replace(tzinfo=None) - t
                
            try:  subject = re.search('subject:([^\n]*)\n', mes, re.I).group(1).strip()
            except (IndexError, AttributeError), e:
                logging.debug(e)
                subject = '(no subject)'      

            snippets.insert(0, {'id': message.id,
                                'subject': subject,
                                'to': to_l,
                                'date': date.strftime('%I:%M %p, %x')                        
                                })  
        return snippets
    
    def get_to_with_links(self, message):
        '''
        Return tuples of prettified recipients with appropriate links
        @param DBEmail, the email 
        @return: [(link_text, destination), ...]
        '''
        # get to addresses and hyperlink
        to_l =[]
        not_here = []
        for r in message.gus_receivers.all():
            name = r.get_full_name()
            username = r.username
            to_l.append(('%s (%s)' % (name, username),
                         '/email/send/%s' % r.pk))
            not_here.extend(name.split())
            not_here.extend(username.split())
            not_here.extend(r.getEmail().split())
        
        # mailto: or no links for non-gus users
        try:
            for r in eval(message.recipients):
                if r not in not_here: to_l.append((r,None))
        except Exception, e:
            logging.debug(e)
        
        return to_l   
    
    def delete_message(self, emailid):
        '''Delete a specified email message
            @param int, the email UID to delete
            @return: boolean success
        '''        
        try:
            message = DBEmail.objects.get(id=emailid)
            message.delete_email(self.user)
        except:
            return False
        
        return True
        
    def check_message(self, emailid):
        '''Check for a specified email message and return it
            @param int, the email UID to get
            @return: mail.EmailMessage
        '''
        
        # get the message from the DB
        try:
            message = DBEmail.objects.filter(models.Q(gus_receivers=self.user)
                              | models.Q(gus_sender=self.user), pk=emailid)[0]
        except Exception, e:
            logging.debug(e)
            return (False, 'This message could not be found on the server, or you do not have permission to view it.')
        
        # parse the message and return it
        try:
            em = self.parse_rfc822(message.header, message.body)
        except KeyError, e:
            logging.debug(e)
            return (True, 'Still retrieving message from messaging server...')
        
        # mark the message as viewed
        try:
            message.view(self.user)
        except Exception, e:
            logging.debug(e)
        
        return em  
    
    def parse_rfc822(self, mes, body=''):
        ''' Parse a message in RFC822 format, split into header and body.
            @param mes: the header in RFC822 format
            @param body: the body (plain text)
            @return: EmailMessage object
        '''
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
                    rm_illegal(to).split(),
                    None)        
        