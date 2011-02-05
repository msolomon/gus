"""
This file runs unit tests on the gus_bill/models.py file.
"""

from django.test import TestCase

class SimpleTest(TestCase):
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
        #test = gus_bill.create(Bname, Bvalue, Ggroup, Guser)
        #if(test.name == "test" && test.value == 11 && test.group == "g1" && test.user == "u1")
        #    return true
        #self.failUnlessEqual(test.value, 11)

    def test_modify_bill(self):
        """
        Tests that the bill from test_create_bill
        Can be modified
        """
        Guser = "u1"
        Ggroup = "g1"
        Bname = "test"
        Bvalue = 11
        self.test_create_bill(self)
        
        #self.failUnlessEqual(gus_bill.modify(Bname, Ggroup, Guser, 12), 12)
        
    def test_get_bill(self):
        """
        Tests that get_bill returns the right bill
        """
        Guser = "u1"
        Ggroup = "g1"
        Bname = "test"
        Bvalue = 11
        test1 = self.test_create_bill(self)
        #test2 = gus_bill.get_bill(Bname, Ggroup, Guser)
        #self.failUnlessEqual(test2, test1)