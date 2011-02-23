from models import bill

class bill_Utils():
    """
    Helper class to create and get bill objects.
    """

    def get_bill(self, Bname, Ggroup, Guser):
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
            (<gus_bill object>)
        """

        return bill.objects.filter(user=Guser, group=Ggroup, name=Bname)
    
    def create_bill(self, Bname, Bvalue, Ggroup, Guser):
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
            (<gus_bill object>)
        """
        #find the bill
        temp = bill.objects.filter(user = Guser, group=Ggroup, name=Bname)
	#used to rename the bill.
	ct = 1
        Bname1 = Bname
        while(len(temp) > 0):
            Bname1 = Bname + ct
            ct += 1
            temp = bill.objects.filter(user = Guser, group=Ggroup, name=Bname1)
        
        return bill.objects.create(user=Guser, group=Ggroup, name=Bname1, value=Bvalue)
        
