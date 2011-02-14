from models import *
from django.db import IntegrityError
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class UsersTest(TestCase):
    
    user = "testuser"
    user_email = "testuser@email.com"
    password = "test"

    def test_create_user(self):
        """
        Test the ability to create a user in the database
        Testing functions found in L{gus_user<gus2.gus_users.models.UserManager.create_user>}    
        """
    
        gus_user.objects.create_user(self.user, self.user_email, self.password)
    
        usr = gus_user.objects.filter(_user__username=self.user)
        #print usr
        #print len(usr)
    
        self.failUnlessEqual(len(usr), 1, "could not create user")
    
    #added 2/11 ~joran
    def test_users_duplicates(self):
        gus_user.objects.create_user(self.user, self.user_email, self.password)
        try:
            gus_user.objects.create_user(self.user, self.user_email, self.password)
        except IntegrityError:
            pass
            return
        self.fail('duplicate users created, this should not happen')
    
    #added 2/11 ~joran
    def test_userAuth(self):
        usr = gus_user.objects.create_user(self.user, self.user_email, self.password)
        self.failUnless(usr.check_password(self.password),"Unable to validate Password")
        
           
    def test_delete_user(self):
        """
        Test the ability to delete a user in the database    
        """

        gus_user.objects.create_user(self.user, self.user_email, self.password)

        usr = gus_user.objects.filter(_user__username=self.user)

        self.failUnlessEqual(len(usr), 1, "could not create user")

        usr[0].delete()
    
        usr = gus_user.objects.filter(_user__username=self.user)
    
        self.failUnlessEqual(len(usr), 0, "could not delete user")
        
        
    # def test_delete_user(self):
    #     """
    #     Test the ability to delete a user in the database    
    #     """
    # 
    #     gus_user.objects.create_user(user, user_email, password)
    # 
    #     usr = gus_user.objects.filter(username = user)
    # 
    #     self.failUnlessEqual(len(usr) == 1, "could not create user")
    # 
    #     usr[0].delete()
    # 
    #     usr = gus_user.objects.filter(username = user)
    # 
    #     self.failUnlessEqual(len(usr) > 1, "could not delete user")    


__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}
