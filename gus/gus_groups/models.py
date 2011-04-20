from django.db import models 

class GroupManager(models.Manager):
    def create(self, groupname, description="", image=""):
        self.create_group(groupname, description, image)

    def create_group(self, groupname, description="", image=""):
        """
        this will create a new group and insert it into the table
        
       
        @type groupname:string
        @param groupname: the name of the new group to create
        @type description:string
        @param description: the description of the group
        @type image:string 
        @param image: the image to associate with the group
        @rtype:gus_roles.models.gus_group
        @return: the newly created group
        
        
            Example
            >>>gus_roles.objects.create_role(<gus_group object>,'group_name')
            (<gus_role object>)
        """
        from utils import makeSlug
        return super(GroupManager, self).get_query_set().create(
            group_name=groupname, group_description=description,
            group_image=image, group_slug=makeSlug(groupname), group_activated=False
            )
    def has_member(self, gusUser):
        """
        this shall return a list of all groups that have the specified 
        user as a member
        
        @type gusUser: gus_users.models.gus_user
        @param gusUser: the user to locate groups for  
        """
        return 1 #placeholder
    

# Create your models here.
# Example documentation for pydoc included
#from gus_roles.models import  gus_role
class gus_group(models.Model):
    """
    class gus_group  is our model of a group
    it shall encompass both the data and discreet functionality of groups
    @author: Joran    
    """

    #Our Fields
        #Django recommends using OneToOne Fields to extend built in models
    group_name = models.CharField(max_length=100,unique=True) #the group name
    group_slug = models.CharField(max_length=100,unique=True) #the url slug for lookup
    
    group_description = models.TextField()         #the group description
    group_image = models.CharField(max_length=50)
    parent_group=models.ForeignKey('gus_group',blank=True,null=True)
    
    group_activated = models.BooleanField()
    
    def getParents(self):
        groups=[]
        p=self.parent_group
        while(p):
            groups.append(p)
            p=p.parent_group
        return groups
    def getChildren(self,recursive=False):
        children=gus_group.objects.filter(parent_group=self)
        if recursive:
            for i in range(0,len(children)-1):
                children[i]=[children[i],self.getChildren(recursive)]
        return children
    def addUser(self,user,role=None):
        """"
        gus_group.addUser(<gus_user>[,<gus_role>]) shall add a user to the given role in the 
        this group, if the <role> argument is ommited it shall add the user as a simple
        Member
         
        @requires: The Group must have the role given (or Member)
        *** all groups created with gus_groups.utils.createNewGroup are automagically given this role
        
        @param user: the user to add to the group
        @type user: <gus_user>
        @param role(Optional):The Group role to add the user to
        @type role:<gus_role> or None
        
        @return: The role that the user has been added to.
        @rtype: <gus_role>      
        """
        
        if not role:
            try:
                from gus_roles.models import gus_role
                r=gus_role.objects.get(_role_group=self,_role_name="Member")
            except:
                print "Error No Role Found"
                return
        r.addUser(user)
        return r
    def output(self): #define verbose output of our group object
        """
        This defines a verbose output display for our group
        ***at the moment this is largely a stub it may or maynot be used 
        @rtype: string
        @return: the verbose output for the group
        """
        return "%s  <br/>\nDescription: %s<br/>\nimage:%s" % (
            self.__unicode__(),
            self.group_description or "(None)",
            self.group_image or "(None)",
            )
    def approveGroup(self):
        self.group_activated=True
        return self
    def getRoles(self):
        """
        return all roles of this group
        """
        from gus_roles.models import gus_role
        return gus_role.objects.filter(_role_group=self)
    def getRole(self,roleName):
        from gus_roles.models import gus_role
        return gus_role.objects.filter(_role_group=self,_role_name=roleName)
    def getUsers(self):
        """
        return all users of this group
        """
        from gus_roles.models import gus_role
        roles = gus_role.objects.filter(_role_group=self)
        return [j for j in [x.users.all() for x in roles ]]

    def delete(self):
	from gus_roles.models import *
	roles = gus_role.objects.filter(_role_group=self)
	for role in roles:
	    role.delete()
	super(gus_group,self).delete()

    objects = GroupManager() # our custom relationships
    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'
        
    def __unicode__(self):
        """
        This defines the default display of a user
        for now we will just return the default django.User display
        
        @rtype:   string
        @return:  the default string for built in django.User.
        """
        return "Group: %s" % self.group_name or '(Not Defined)'
    roles=property(getRoles)
    users=property(getUsers)
    
