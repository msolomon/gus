"""
This file runs unit tests on the gus_bill/models.py file.
"""

from gus2.gus_bill.models import *
from gus2.gus_users.models import *
from gus2.gus_groups.models import *
from django.test import TestCase

class BillTest(TestCase):
    Guser = None
    Ggroup = None
    Bname = "test"
    Bvalue = 50

    def setUp(self):
        self.Guser = gus_user.objects.create_user("u1", "email", "pass")
        self.Ggroup = gus_group.objects.create_group("g1", "email", "pass")
        
    def test_create_bill(self):
        """
        Tests that the bill was created.
        This bill will be named test
        The user will be u1
        The group will be g1
        The initial value will be 11
        """
        test = bill.objects.create_bill(user = self.Guser, group = self.Ggroup, name = self.Bname, value = self.Bvalue)
        t2 = bill.objects.filter(pk = test.id)
        self.failUnless(len(t2) == 1 and t2[0].user == self.Guser, "Could not create bill")
        return test


    def test_payment(self):
        """
        Tests that the bill from test_create_bill
        Can be modified
        """
        Nvalue = 10
        test = self.test_create_bill()
        paid = test.make_payment(Nvalue)
        self.failUnless(paid == 10, "Unable to make payment")

        paid = test.make_payment(Nvalue)
        self.failUnless(paid == 20, "Unable to pay more then once.")
        
        
    def test_modify(self):
        test = self.test_create_bill()
        test.name = "u2"
        test.save()
        t2 = bill.objects.filter(pk = test.id)
        self.failUnless(len(t2) == 1 and t2[0].name == "u2", "Unable to modify bill")

    def test_delete(self):
        test = self.test_create_bill()
        test.delete()
        t2 = bill.objects.filter(pk = test.id)
        self.failUnless(len(t2) == 0, "Unable to delete.")
        
    def test_many_bill(self):
        test = self.test_create_bill()
        Nvalue = 75
        Nname = "test2"
        test2 = bill.objects.create_bill(user = self.Guser, group = self.Ggroup, name = Nname, value = Nvalue)
        t2 = bill.objects.filter(user = self.Guser)
        self.failUnless(len(t2) == 2, "Unable to create second bill for same user.")

    def test_same_name(self):
        test = self.test_create_bill()
        test2 = self.test_create_bill()
        self.failUnless(test.id > 0 and test2.id > 0 and test.name != test2.name, "Identical bill creation error.")
