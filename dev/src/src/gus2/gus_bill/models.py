from django.db import models
#I'm pretty sure more should be here

class bill():
    """
    Used to keep track of billing for groups.
    Does not make payments or handle money.
    """

    def create_bill(Bname, Bvalue, Ggroup, Guser):
        """
        This creates a new bill.  Associates it with the given
        Ggroup, Guser, Bname; and gives it the specified Bvalue
        @type Guser: gus_users.models.gus_user
        @param Guser: Name of the user associated with the bill
        @type Ggroup: gususers.modles.gus_group ??
        @param Group: Name of the group associated with the bill 
        @type Bname: string 
        @param Bname: Name of the bill (to allow for more than 1 per user) 
        @type Bvalue: int
        @param Bvalue: Ammount the make the bill for
        Example:
            >>>create_bill(test, 11, g1, u1)
        """
        return gus_bill.objects.create(user=Guser, group=Ggroup, name=Bname, value=Bvalue)

    def get_bill(Bname, Ggroup, Guser):
        """
        Returns the bill associated with the Ggroup, Guser, and Bname
        @type Guser: gus_users.models.gus_user
        @param Guser: Name of the user associated with the bill
        @type Ggroup: gususers.modles.gus_group ??
        @param Group: Name of the group associated with the bill 
        @type Bname: string 
        @param Bname: Name of the bill (to allow for more than 1 per user) 
        Example:
            >>>get_bill(test, g1, u1)
        """
        return gus_bill.objects.filter(user=Guser, group=Ggroup, name=Bname)

    def modify_bill(Bname, Bvalue, Ggroup, Guser):
        raise Exception("In Development", "This function does not work, yet.")
        """
        Changes the ammound of the bill associated with
          the Ggroup, Guser, and Bname to the Bvalue
        @type user: gus_users.models.gus_user
        @param user: name of the user to create the bill for
        @type ammout: double
        @param ammount: ammount of currency previously due the user
        @type new: double
        @param ammount: ammount of currency due the user
        @return: none

        Example:
            >>>modify_bill(test, g1, u1, 12)
        """
        mod = get_bill(Bname, Ggroup, Guser)
        mod.value = Bvalue
        mod.save()
        return mod.value