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
        Testing functions found in L{gus_user<gus.gus_users.models.UserManager.create_user>}    
        """
    
        gus_user.objects.create_user(self.user, self.user_email, self.password)
    
        usr = gus_user.objects.filter(_user__username=self.user)
        #print usr
        #print len(usr)
    
        self.failUnlessEqual(len(usr), 1, "could not create user")
    
    #added 2/11 ~jora    n
    def test_users_duplicates(self):
        """
        test user duplication, this should not be allowed and will fail if 
        it successfully adds multiple users with same user name
        """
        gus_user.objects.create_user(self.user, self.user_email, self.password)
        try:
            gus_user.objects.create(self.user, self.user_email, self.password)
        except IntegrityError:
            pass
            return
        self.fail('duplicate users created, this should not happen')
    def test_user_slow_initialize(self):
        usr = gus_user()
        
        self.failUnless("%s"%usr=="user: (Undefined User)")
        
        
    def test_setters(self):    
        usr = gus_user.objects.create_user(self.user, self.user_email, self.password)
        usr.username="bob1"
        usr = gus_user.objects.get(pk=1)
        self.failUnless((usr.username == "bob1"),'Error with Username getter/setter')
        usr.first_name="bobFN"
        usr = gus_user.objects.get(pk=1)
        self.failUnless((usr.first_name == "bobFN"),'Error with first_name getter/setter')
        
        usr.first_name="smithLN"
        usr = gus_user.objects.get(pk=1)
        self.failUnless((usr.first_name == "smithLN"),'Error with last_name getter/setter')
        
        usr.email="smith@email"
        usr = gus_user.objects.get(pk=1)
        self.failUnless((usr.email== "smith@email"),'Error with email getter/setter')
        
        
        usr = gus_user.objects.get(pk=1)
        
        try:
            usr.user = "a"
        except:#here we expect exception
            pass 
            return 
        self.fail('Able to set readonly user property')
        
        
    def test_unicode(self):
        usr = gus_user.objects.create_user(self.user, self.user_email, self.password)
        self.failUnless((usr.__unicode__()=="User: %s"%self.user),"Error With unicode")
    #added 2/11 ~joran
    def test_userAuth(self):
        """
        Test Basic User Authentication (specifically password validity)
        """
        usr = gus_user.objects.create_user(self.user, self.user_email, self.password)
        self.failUnless(usr.check_password(self.password),"Unable to validate Password")
        usr.set_password("testpw2")
        self.failUnless(usr.check_password("testpw2"),"Unable to change Password")
        
        #try and illegally manually set userid
        try:
            usr.setID(1)
        except:#here we expect exception
            pass 
            return 
        self.fail('Able to set readonly user property')
        
        
    def test_Unuseable_pw(self):
        """
        test the unusable password features
        """
        usr = gus_user.objects.create_user(self.user, self.user_email, self.password)
        usr.set_unusable_password()
        self.failUnless(not usr.has_usable_password(), "Unusable Password Failure")
    
    def test_get_full_name(self):
        usr = gus_user.objects.create_user(self.user, self.user_email, self.password)
        usr.first_name="test"
        usr.last_name="user"
        str = usr.first_name,usr.last_name
        self.failUnless(usr.get_full_name()=="test user","could not retrieve full name")
        
    def test_anonUser(self):
        """
        Test Anonomous User
        """
        usr = gus_user.objects.create_user(self.user, self.user_email, self.password)
        self.failUnless(not usr.is_anonymous(), "User is created and is still anon")
        
    def test_authenticated(self):
        usr = gus_user.objects.create_user(self.user, self.user_email, self.password)
        self.failUnless( usr.is_authenticated(), "User is created and is still not authenticated")    
    
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
