from django.db import models
from django.contrib.auth.models import User



class UserManager(models.Manager):
    def create(self, username, email, password):
        self.create_user(username, email, password)

    def create_user(self, username, email, password):
        """
        this will create a new user and insert it into the table
        
        @type username:string
        @param username: The Username of the user to add
        @type email:string
        @param email: The email of the user to add
        @type password:string
        @param password: the plaintext password for the user to add
        @rtype:gus_roles.models.gus_user
        @return: the newly created user
        
        
                   
            >>>gus_user.objects.create_user('username','email','password')
            (<gus_user object>)
        """
        usr = User.objects.create_user(username, email, password);
        
        return super(UserManager, self).get_query_set().create(
            _user=usr, bio='',
            )
        
# Create your models here.
# Example documentation for pydoc included
class gus_user(models.Model):
    """
    class gus_user model is our model of a user of the gus system
    
    it shall encompass all of the data and 
    all of the discreet functionality of use of the gus system    
    """

    ###############################################
    #         -= Our Fields =-                   ###
    #################################################
    #    Django recommends using OneToOne Fields ######
    # to extend built in models.                 ########
    # our key is remote record of builtin        ###########
    # django.contrib.auth.User                   ###############
    # single underscores signifies private variables (sort of)##
    # double underscores will cause              ###############
    #        name mangling which is ok sometimes ########
    #################################################
    
    _user = models.OneToOneField(User, primary_key=True)  
    bio = models.TextField()    # Sample Extension Field
    roles = models.ManyToManyField('gus_roles.gus_role')

    #################################################
    ####  Methods specific to gus users  ####
    #################################################      
    
     

    #################################################
    ####  django.contrib.auth.models.User hooks  ####
    #################################################      
    
    def is_anonymous(self):
        """
        Always returns false. you should not have an anonymous user
        except in the case that it is a django.anonUser
        
            Note* per django documentation you should defer to is_authenticated
            
        @see: L{django.contrib.auth.models.AnonymousUser<AnonymousUser>}
        @see: L{django.contrib.auth.models.User.is_anonymous<User.is_anonymous>}
        @return: False
        """
        
        return self._user.is_anonymous()
    
    def is_authenticated(self):
        """
        Always returns true. you should not have an un authenticated user
        except in the case that it is a django.anonUser
        @see: L{django.contrib.auth.models.AnonymousUser<AnonymousUser>}
        @see: L{django.contrib.auth.models.User.is_authenticated<User.is_authenticated>}
        @return: True
        """
        return self._user.is_authenticated()
    def group_role(self,group):
        """
        return the role that this use holds within the given group or none
        
        """
        from gus_roles.models import gus_role
        return gus_role.objects.with_user_in_group(group,self)
    
    def has_group_perm(self,group,perm):
        """"
        determine if this user has a given permision for a given group
         
        """
        
        r = self.group_role(group)
        try:
            return r.has_perm(perm)
        except:
            return self.has_groups_perm(group, perm)
    def has_groups_perm(self,group,perm):
        """
        determine if this user has a given permission for this group or any of its parent groups
        """
        groups = group.getParents()
        #print "Check Parent Permissions :",perm
        #print groups
        for g in groups:
            if self.has_group_perm(g,perm): return True
        return False
    
    def get_full_name(self):
        """
        return the users full name
        """
        return self._user.get_full_name()
    
    def set_password(self, raw_password):
        """
        Set the users password , expects unencoded password
        """
        return self._user.set_password(raw_password)
    
    def check_password(self, raw_password):
        """
        checks unencoded passsword against expected
        """
        return self._user.check_password(raw_password) 
    
    def set_unusable_password(self):
        """
        create a user that cannot login (or disable login for existing)
        """
        return self._user.set_unusable_password()
    
    def has_usable_password(self):
        return self._user.has_usable_password() 
    
    def has_perm(self, perm, obj=None):
        return self._user.has_perm(perm, obj) # pragma : no cover
    
    def has_perms(self, perm_list, obj=None):
        return self._user.has_perms(perm_list, obj) # pragma : no cover
    
    def has_module_perms(self, package_name):
        return self._user.has_module_perms(package_name)  # pragma : no cover
    
    def get_and_delete_messages(self):
        return self._user.get_and_delete_messages() # pragma : no cover
    
    def email_user(self, subject, message, from_email=None):
        return self._user.email_user(subject, message, from_email) # pragma : no cover
    
    def get_profile(self):
        return self._user.get_profile() # pragma : no cover

    def add_role(self, role):       
        role.save()
                                    
    #################################################
    ####  Python Magic Functions       ##############
    #################################################
    objects = UserManager()     
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'                                     
    #define how to display our object in the html
    def __unicode__(self):
        """
        This defines the default display of a user
        for now we will just return the default django.User display
        
        @rtype:   string
        @return:  the default string for built in django.User.
        """
        
        try:
            return "User: %s" % self.user
        except:
            return "user: %s" % '(Undefined User)'
     
    
    
    ################################################
    ###   Getters And Setters ######################
    ################################################
    #Define our setters , syntax is:def setProperty(self): ... 
    #    s.t. Property is the name of the property you wish to use 
    #  a setter for , with the first letter capitalized
    
    #setter for our user
    def setUser(self, user):
        """
        Set our user
        
        @type user:django.contrib.auth.models.User
        @param user: the user to parent to this instance
        @rtype: none 
        """
        raise Exception('UserPerimissionError', 'This Attribute is READ-ONLY')
        
    #setter for our username
    def setUsername(self, value):
        """
        Set our user.username
        
        @type  value: string
        @param value: the new username.
        @rtype: None
        """
        self._user.username = value
        self._user.save()
    def setEmail(self,value): 
        self._user.email = value
        self._user.save()
    def setFN(self,value):
        self._user.first_name = value
        self._user.save()
    def setLN(self,value):
        self._user.last_name = value
        self._user.save()
               
    def setID(self,value):
        """
        setter hook for ID to disallow changing
        """
        raise Exception('UserPerimissionError', 'This Attribute is READ-ONLY')
    #Define our getters , syntax is:def getProperty(self): ... 
    #    s.t. Property is the name of the property you wish to use
    #  a getter for, with the first letter capitalized
    
    #getter for our username
    def getUsername(self):
        """
        Return our user.username
        
        @rtype: string
        @return: the value of our parent user's username
        """
        return self._user.username
    
    #getter for our user
    def getUser(self):
        """
        Return our user
        
        @rtype: django.contrib.auth.models.User
        @return: the value of our parent user
        """
        return self._user

    def getRoles(self):
        """
        return all roles associated with group
        """
        from gus_roles.models import gus_role
        
        return gus_role.objects.filter(_role_users=self._user.id)
    
    def getID(self):
        return self._user.id
    
    def getEmail(self):
        return self._user.email
    def getFN(self):
        return self._user.first_name
    def getLN(self):
        return self._user.last_name
    
    #GETTER/SETTER enabled ... hackish
    #GETTERS AND SETTERS WILL BE USED (!Include simillar code in all classes)
    #getter and setter hooks , these must be setup if you wish to 
    #use gus_user.<property> = <blah>  or print gus_user.<property>
    # A Hack to make variables use setter
    
    #user hook
    user = property(getUser, setUser)
    id = property(getID, setID)
    #username hook
    username = property(getUsername, setUsername)
    email = property(getEmail, setEmail)
    first_name = property(getFN, setFN)
    last_name = property(getLN, setLN)
    roles = property(getRoles, None)
