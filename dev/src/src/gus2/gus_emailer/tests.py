from django.test import TestCase
from time import localtime, strftime
from gus2.gus_emailer.models import *

class EmailSystemTest(TestCase):
    def test_emailer(self):
        emailer = Emailer()
        timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        emailer.send_message('[test] %s' % timestamp,
                             'This is only a test!',
                             'guspyuser@gmail.com')
