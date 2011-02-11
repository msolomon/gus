from django.db import models 

class GroupManager(models.Manager):
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
            group_image=image, group_slug=makeSlug(groupname)                                                   
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
class gus_group(models.Model):
    """
    class gus_group  is our model of a group
    it shall encompass both the data and discreet functionality of groupss    
    """
    
    #Our Fields
        #Django recommends using OneToOne Fields to extend built in models
    group_name = models.CharField(max_length=100,unique=True) #the group name
    group_slug = models.CharField(max_length=100,unique=True) #the url slug for lookup
    
    group_description = models.TextField()         #the group description
    group_image = models.CharField(max_length=50)
    
    
    
    def output(self): #define verbose output of our group object
        """
        This defines a verbose output display for our group
        @rtype: string
        @return: the verbose output for the group
        """
        return "%s  <br/>\nDescription: %s<br/>\nimage:%s" % (
            self.__unicode__(),
            self.group_description or "(None)",
            self.group_image or "(None)",
            )
                
    
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

    
