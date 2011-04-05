# Put Helper Functions for groups here 
# dont forget to include any classes you may need


def makeSlug(slug):
    """
    replaces spaces with underscores and makes the string lowercase
    
    @type slug:string
    @param slug:the normal string with mixed upper/lower case and spaces
    @rtype: string
    @return: the string with all lowercase and spaces replaced with underscores  
    """
    return slug.replace(' ', '_').lower()

def createNewGroup(owner, group_name="", group_desc="", group_image=""):
    """
    creates a new group and the default roles associated with it
    @param owner: the user who is the owner of this group
    @param group_name: the name for this group
    @param group_desc: the description for this group
    @param group_image: the image for this group
    @return:  the new group    
    """
    from gus.gus_groups.models import gus_group
    from gus.gus_roles.models import gus_role
    grp = gus_group.objects.create_group(group_name, group_desc, group_image)
    
    #create our default roles
    #create owner role
    r1 = gus_role.objects.create_role(grp, 'Owner')
    r1._role_permission_level = 10
    r1.save()
    r1.addUser(owner)
    #create Super-User Role
    r2 = gus_role.objects.create_role(grp, 'Super-User')
    r2._role_permission_level = 1
    r2.save()
    #Create Regular Member Role
    r3 = gus_role.objects.create_role(grp, 'Member')
    
    return grp
    
def getGroupRoles(group):
    """
    return all the roles (with users) for a given group
    @param group: the group to return the roles of
    @return: a query set of roles that the group is associated with 
    """
    from gus.gus_roles.models import gus_role
    return gus_role.objects.with_group(group)

def getGroupsWithUser(usr):
    """
    return a list of groups with user as a member
    
    @type user: gus_users.models.gus_user
    @param user: the user to fetch the groups for
    @rtype: queryset
    @return: list of groups that have this user as a member 
    """
    if usr.is_anonymous() : return []
    from gus.gus_roles.models import gus_role
    return map(lambda x:  x._role_group , gus_role.objects.with_user(usr))



def setDiff(src_set, set2):
    """
    helper function, yeilds the difference of two sets src_set should be the larger of the two
    @param src_set: the first set (should be the larger of the two)
    @param set2: the second set (should be the smaller of the two)
    @return: a set that contains elements in src_set that are not in set2  
    """
    a = []
    for elem in src_set:
        if not set2.__contains__(elem):a.append(elem)
    return a
