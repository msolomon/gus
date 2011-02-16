from django.db import models
from django.contrib.auth.models import Group
from gus.gus_groups.models import gus_group
from gus.gus_users.models import gus_user
# Create your models here.

class RoleManager(models.Manager):
    def create_role(self, group, role_name):
        """
        this will create a new role and insert it into the table
        
        @type group:gus_groups.models.gus_group
        @param group: the group to associate with the role
        @rtype:gus_roles.models.gus_role
        @return: the newly created role
        
        
            >>>gus_roles.objects.create_role(<gus_group object>,'group_name')
            (<gus_role object>)
        """
        django_grp = Group.objects.create(
                name="%s.%s" % (group.group_name, role_name)
                )
        newrole = gus_role.objects.create(
            _role_permissions=django_grp,
            _role_group=group,
            _role_name=role_name
            )                                                            
        
        return newrole
        
    
    def with_user_in_group(self, group, user):
        """
        will return 1 role or false depending on if the given user 
        has a role in the given group
        
        @type group:gus_groups.models.gus_group
        @param group: the group in question
        @type user:gus_groups.models.gus_user
        @param user: the user in question
        """
        return super(RoleManager, self).get_query_set().filter(
                _role_users=user,
                _role_group=group,
        )
    
    def with_user(self, user):
        """
        will return all roles of a given user
        @param user: The user to find the groups for
        @type user: L{gus_user<gus.gus_users.models.gus_user>}
        @rtype: List
        @return: a set of all groups that a given user belongs to 
        """
        return super(RoleManager, self).get_query_set().filter(
                _role_users=user,
        )
    def users_without_group(self, group):
        #roles_in_group
        roleswgrp = self.with_group(group);
        id_list = []
        for role in roleswgrp:
            id_list.extend(map(lambda x: x.id , role.users.all()))
        return gus_user.objects.exclude(_user__in=id_list)
        
    def users_with_group(self, group):
        """
        will return all users of a given gus_group
        @param group: The group to find the users for
        @type group: L{gus_group<gus.gus_groups.models.gus_group>}
        @rtype: List
        @return: a set of all users that a given group has
            Ex.
            >>>gus_role.objects.users_with_group(group1)
            (<user1>,<user2>,...,<userN>)
        """
        roleswgrp = self.with_group(group);
        id_list = []
        for role in roleswgrp:
            id_list.extend(map(lambda x: x.id , role.users.all()))
        return gus_user.objects.filter(_user__in=id_list)
        
            
    def with_group(self, group):
        """
        will return all roles of a given group
        """
        return super(RoleManager, self).get_query_set().filter(
                _role_group=group,
        )
    
    
    

        
class gus_role(models.Model):
    """
    class gus_role  is our model of a groupRole
    it shall encompass both the data and discreet functionality of groupRoles
    GroupRoles are used to tie users and groups together 
    and to provide permissions within a group context    
    """
    
    
    ###############################################
    ####   Model Fields ###########################
    ###############################################
    
    # double underscore is essentially a private variable
    _role_users = models.ManyToManyField(gus_user) #ManyToMany relationship....
    
    #since django's built in groups are simillar to our roles we will
    
    #simply make our permissions an instance of traditional group permisions
    _role_permissions = models.OneToOneField(Group)
    
    #essentially ManyToOne Relationship
    _role_group = models.ForeignKey(gus_group) 
    
    #textual name of the role (ie:Admin,User,etc)
    _role_name = models.CharField(max_length=100)
    
    #we can use this for special flags
    _role_permission_level = models.IntegerField(default=0)
    
    #################################################
    #### Gus Roles Specific Functions       #########
    #################################################
    def addUser(self, user):
        """
        this will add a user to a role
        @type user:gus_users.models.gus_user
        @param user:the user to add to the role
        @rtype: gus_roles.models.gus_role
        @return: the role , with the new user added to the list  
        """
        user.add_role(self)
        self._role_users.add(user)
    def removeUser(self, user):
        """
        this will remove a user from a role
        @type user:gus_users.models.gus_user
        @param user:the user to add to the role
        @rtype: gus_roles.models.gus_role
        @return: the role , with the user removed from the list  
        """
        self._role_users.remove(user)
    
    #################################################
    ####  Python Magic Functions       ##############
    #################################################
    
    objects = RoleManager() #defines custom associations                                            
    def permString(self):
        """
        return a list of permissions associated with this role
        as a comma separated string
        
        @rtype: string
        @return: Comma seperated string listing of our permissions
        """
        perms = self._role_permissions.permissions.all()
        if not perms.count() : return ""
        permList = [] 
        for perm in perms:
            permList.append(perm)
        return " '%s'" % "', '".join(map(lambda x:x.name, permList));
    
    def has_perm(self,perm):
        """
        determine if this role has a given permission
         
        @type perm:string
        @param perm:the permission to checkfor
        @rtype: boolean
        @return: True or False Depending on whether the role has the permission  
        """
        perms = self._role_permissions.permissions.all()
        if not perms.count() : return False
        for i in perms:
            if i == perm: return True
        return False
    
    #define how to display our object in the html
    def __unicode__(self):
        """
        This defines the default display of a role
        for now we will just return the default django.User display
        
        @rtype:   string
        @return:  the default string for built in django.User.
        """
        
        return 'Role :[%s] %s ' % (self._role_group.group_name, self._role_name) 
    
    
    ################################################
    ###   Getters And Setters ######################
    ################################################
    #Define our setters , syntax is:def setProperty(self): ... 
    #    s.t. Property is the name of the property you wish to use 
    #  a setter for , with the first letter capitalized
    
    #setter for our user
    def setUsers(self, user):
        """
        return an error about being read only
        """
        raise Exception, "RoleUsersPermisionError: This Property is read Only" # pragma : no cover
    def setGroup(self):
        """
        return an error about being read only
        """
        raise Exception, "RoleUsersPermisionError: This Property is read Only" # pragma : no cover
    #Define our getters , syntax is:def getProperty(self): ... 
    #    s.t. Property is the name of the property you wish to use
    #  a getter for, with the first letter capitalized
    
    
    
    #getter for our users
    def getUsers(self):
        """
        Return our users
        
        @rtype: django.contrib.auth.models.User
        @return: the value of our parent user
        """
        return self._role_users
    #getter for our user
    def getGroup(self):
        """
        Return our group
        
        @rtype: django.contrib.auth.models.User
        @return: the value of our parent user
        """
        return self._role_group
    
    #GETTER/SETTER enabled ... hackish
    #GETTERS AND SETTERS WILL BE USED (!Include simillar code in all classes)
    #getter and setter hooks , these must be setup if you wish to 
    #use gus_user.<property> = <blah>  or print gus_user.<property>
    # A Hack to make variables use setter
    
    #users hook
    users = property(getUsers, setUsers)
    group = property(getGroup, setGroup)
