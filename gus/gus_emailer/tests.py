from django.test import TestCase
from django.core import mail
from time import localtime, strftime
from gus.gus_emailer.models import *
from gus.gus_users.models import *
from gus.gus_groups.utils import *

class EmailSystemTest(TestCase):
    def setUp(self):
        owner = gus_user.objects.create_user('owner', 'anonymous-user@guspy.joranbeasley.com', 'password')
        member = gus_user.objects.create_user('testuser', 'guspyuser@guspy.joranbeasley.com', 'password')
        grp = createNewGroup(owner, 'My awesome group', 'test group')
        roles = getGroupRoles(grp)
        roles[2].addUser(member)
        self.usr = gus_user.objects.get(pk=1) # should be owner
        
    def test_emailer(self):
    	'''Test the email system.
    	
    		Django overrides the backend to be in-memory during testing,
    		so smtp connections are not tested
    	'''
    	connection = mail.get_connection(backend='django.core.mail.backends.locmem.EmailBackend')
        emailer = Emailer(self.usr)
        timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        emailer.send_message('[test] %s' % timestamp,
                             'This is only a test!',
                             [self.usr.getEmail()],
			     connection=connection)
        self.failIfEqual(len(mail.outbox), 0, 'Message not sent!')
	connection.close()

    def test_imap(self):
        ''' Test the IMAP4 email checking system
        '''
        em = Emailer(self.usr)
        messages = None
        try:
            messages = em.check_email()
        except:
            pass
        
        self.failIfEqual(messages, None,
                "No messages could be retrieved!")

    def test_group(self):
        ''' Send an email to a group '''
        connection = mail.get_connection(backend='django.core.mail.backends.locmem.EmailBackend')
        emailer = Emailer(self.usr)
        timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        testmessage = mail.EmailMessage('[test] %s' % timestamp,
                             'This is a group test.',
                             self.usr.getEmail(),
                             [],
                             [],
                 connection=connection)
        groups = [x.group for x in gus_role.objects.with_user(self.usr)]
        for group in groups:
            emailer.sendto_group(testmessage, group)
        self.failIfEqual(len(mail.outbox), 0, 'Message not sent!')
        connection.close()
