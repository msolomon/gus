from django.test import TestCase
from django.core import mail
from time import localtime, strftime
from gus2.gus_emailer.models import *

class EmailSystemTest(TestCase):
    def runTest(self):
	pass

    def test_emailer(self):
	'''Test the email system.
	
		Django overrides the backend to be in-memory during testing,
		so smtp connections are not tested
	'''
	connection = mail.get_connection(backend='django.core.mail.backends.locmem.EmailBackend')
        emailer = Emailer()
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
	em = Emailer()
	em.set_imap('imap.gmail.com', 993)
	em.set_imap_user('guspyuser@gmail.com', 'givemegus')

	messages = em.check_email()
	self.failIfEqual(len(messages), 0,
			"No messages could be retrieved!")

	# for ident, message in response.iteritems():
	# 	print message['RFC822']
	
