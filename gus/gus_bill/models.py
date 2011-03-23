from django.db import models
from gus.gus_users.models import gus_user
from gus.gus_groups.models import gus_group
from django.db.models import Sum

class payment(models.Model):
    """
    Used to hold values for payments, can only be associated with one bill.
    """

    #requires that all payments be associated with a valid bill object
    mybill = models.ForeignKey("bill")

    #fields to be searched by later    
    amtpaid = models.FloatField()
    datepaid = models.DateField(auto_now_add = True)

class BillManager(models.Manager):
    def create_bill(self, user, group, name, value):
        """
        This will create a new user and insert it into the table
        
        @type user: string
        @param user: The Username associated with this bill
        @type group: string
        @param group: The Group the bill is associated with
        @type name: string
        @param name: The name of the bill to be added
        @type value: double
        @param value: The value of the bill.
        @rtype: gus_roles.models.gus_user
        @return: the newly created user
        
        
                   
            >>>gus_bill.objects.create_bill('username','group','name', value)
            (<gus_bill object>)
        """
        #gets all of the bills which match the user, group, and name asked for in creation
        temp = super(BillManager, self).get_query_set().filter(user = user, group = group, name = name)
        ct = 1
        Bname1 = name
        #check and see if the same bill already exists
        #if it does, rename this bill to be test1, test2, test3 ect.
        while(len(temp) > 0):
            Bname1 = name + str(ct)
            ct += 1
            temp = super(BillManager, self).get_query_set().filter(user = user, group=group, name=Bname1)
        
        #call the constructor in untils.py
        return super(BillManager, self).get_query_set().create(user=user, group=group, name=Bname1, value=value)
                


class bill(models.Model):
    """
    Used to keep track of billing for groups.
    Does not handle money, only track numbers and changes.
    """
    #these create fields which can be used to filter for the bill later
    #requires that groups and users be valid gus_groups and gus_users
    user = models.ForeignKey(gus_user)
    group = models.ForeignKey(gus_group)
    name = models.CharField(max_length = 100)
    value = models.FloatField()
    #auto_now_add = true means that when the bill is created
    #  this will be set to the current time, and only when
    #  the bill is created.
    datecreated = models.DateField(auto_now_add = True)


    objects = BillManager()


    def paid_balance(self):
        """
        Returns the sum of the payments.
        
        @type temp: int
        @param temp: A total value of the ammount paid to the associated bill
        @rtype: int
        @return: sum of payments (or 0 if no payments have been made)

            >>>paid_balance()
            x
        """
        #get all payment objects associated with this bill
        temp = payment.objects.filter(mybill = self).aggregate(Sum('amtpaid'))
        #verify there exists payment objects
        if(temp["amtpaid__sum"]):
            return temp["amtpaid__sum"]
        return 0

    def make_payment(self, Bvalue):
        """
        Adds to the list of payments that have been made to the current bill.
        
        @type ammout: double
        @param ammount: ammount of currency previously due the user
        @return: sum of payments made to this bill

            >>>make_payment(value)
            x
        """
        #verify the ammount to be paid is not greater than the total balance
        if(Bvalue + self.paid_balance() > self.value):
            return self.paid_balance()
        #create a payment object associated with this bill
        payment.objects.create(mybill = self, amtpaid = Bvalue)
        return self.paid_balance()

    def delete(self):
        """
        Overrides the original delete function, to make sure that all of
          the payment objects also get deleted.

            >>>bill.delete()
        """
        #will delete every payment object associated with this bill
        payment.objects.filter(mybill = self).delete()
        #uses the default delete function to delete the bill
        super(bill, self).delete()
        
    #used for the views output
    def __unicode__(self):
	return "%s, %s: $%.2f"%(self.user, self.name, self.value)






