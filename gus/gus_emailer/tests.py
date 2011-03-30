from django.test import TestCase
from django.core import mail
from time import localtime, strftime
from gus.gus_emailer.models import *
from gus.gus_users.models import *
from gus.gus_groups.utils import *

class EmailSystemTest(TestCase):
    def setUp(self):
        owner = gus_user.objects.create_user('owner', 'guspyuser@gmail.com', 'password')
        member = gus_user.objects.create_user('testuser', 'guspyuser@gmail.com', 'password')
        grp = createNewGroup(owner, 'My awesome group', 'test group')
        roles = getGroupRoles(grp)
        roles[2].addUser(member)
        self.usr = gus_user.objects.get(pk=1)
        
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
                             ['guspyuser@gmail.com'],
			     connection=connection)
        self.failIfEqual(len(mail.outbox), 0, 'Message not sent!')
	connection.close()

    def test_imap(self):
    	''' Test the IMAP4 email checking system
    	'''
    	em = Emailer(self.usr)
    
    	messages = em.check_email()
    	self.failIfEqual(len(messages), 0,
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
        emailer.sendto_group(testmessage)
        self.failIfEqual(len(mail.outbox), 0, 'Message not sent!')
	connection.close()
