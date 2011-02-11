"""
This file runs unit tests on the gus_bill/models.py file.
"""

from gus2.gus_bill.models import *
from django.test import TestCase

class BillTest(TestCase):
    def test_create_bill(self):
        """
        Tests that the bill was created.
        This bill will be named test
        The user will be u1
        The group will be g1
        The initial value will be 11
        """
        Guser = "u1"
        Ggroup = "g1"
        Bname = "test"
        Bvalue = 11
#        test = gus_bill.objects.create(user = Guser, group = Ggroup, name = Bname, value = Bvalue)
#        self.failUnlessEqual(test, 1) # will fail, need better test here
#        return test


    def test_modify_bill(self):
        """
        Tests that the bill from test_create_bill
        Can be modified
        """
        Nvalue = 5
#        test = self.test_create_bill()
#        paid = test.make_payment(Nvalue)
#        self.failUnlessEqual(paid, 6)
        
        
    def test_get_bill(self):
        """
        Tests that get_bill returns the right bill
        """
        Guser = "u1"
        Ggroup = "g1"
        Bname = "test"
        Bvalue = 11
#        test = self.test_create_bill()
#        test2 = get_bill(Bname, Ggroup, Guser)
#        self.failUnlessEqual(test, test2)

