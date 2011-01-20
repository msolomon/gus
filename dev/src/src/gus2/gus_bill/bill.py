from django.db import models

class bill():
    """
    used to keep track of billing for groups.

    @type id: int
    @var id: the id number of this bill
    @type group_id: int
    @var group_id: the id number of the group associated with this bill
    @type user_id: int
    @var user_id: the id number of the user associated with this bill
    @type name: string
    @var name: the name of this bill
    @type date_created: datetime
    @var date_created: the time/day this bill was created
    @type ammount: double
    @var ammount: the ammount of currency this bill is
    """
#    id
#    group_id
#    user_id
#    name
#    date_created
#    ammount

    def __init__(self, user, name, ammount):
        raise Exception("In Development", "This function does not work, yet.")
         #not sure how to get these values.
#        id = ??
#        group_id = ?
#        user_id = ?
#        self.date_created = ?

#        self.name = name
#        self.ammount = ammount


    """
    the following retur their respective variables
    """
    def get_id(self):
        """
        @rtype: int
        @return: self.id
        """
#        return self.id

    def get_group_id(self):
        """
        @rtype: int
        @return: self.group_id
        """
#        return self.group_id
        
    def get_user_id(self):
        """
        @rtype: int
        @return: self.user_id
        """
#        return self.user_id
        
    def get_name(self):
        """
        @rtype: string
        @return: self.name
        """
#        return self.name
        
    def get_date_created(self):
        """
        @rtype: datetime
        @return: self.date_created
        """
#        return self.date_created
        
    def get_ammount(self):
        """
        @rtype: double
        @return: self.ammount
        """
#        return self.ammount


    def modify_bill(self, ammount):
        raise Exception("In Development", "This function does not work, yet.")
        """
        this will change the ammout for this bill to the new ammount

        @type user: gus_users.models.gus_user
        @param user: name of the user to create the bill for
        @type ammout: double
        @param ammount: ammount of currency previously due the user
        @type new: double
        @param ammount: ammount of currency due the user
        @return: none

        Example:
            >>>???
        """
#        self.ammount = ammount 
