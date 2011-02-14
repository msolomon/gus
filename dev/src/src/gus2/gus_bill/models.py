from django.db import models
from gus2.gus_users.models import gus_user
from gus2.gus_groups.models import gus_group
from django.db.models import Sum

class payment(models.Model):
    
    mybill = models.ForeignKey("bill")
    
    amtpaid = models.FloatField()
    datepaid = models.DateField(auto_now_add = True)

class BillManager(models.Manager):
    def create_bill(self, user, group, name, value):
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
        
        temp = super(BillManager, self).get_query_set().filter(user = user, group = group, name = name)
        ct = 1
        Bname1 = name
        while(len(temp) > 0):
            Bname1 = name + str(ct)
            ct += 1
            temp = super(BillManager, self).get_query_set().filter(user = user, group=group, name=Bname1)
        
        return super(BillManager, self).get_query_set().create(user=user, group=group, name=Bname1, value=value)
                


class bill(models.Model):
    """
    Used to keep track of billing for groups.
    Does not make payments or handle money.
    """
    user = models.ForeignKey(gus_user)
    group = models.ForeignKey(gus_group)
    name = models.CharField(max_length = 100)
    value = models.FloatField()
    datecreated = models.DateField(auto_now_add = True)


    objects = BillManager()


#COMMENT THIS!
    def paid_balance(self):
        temp = payment.objects.filter(mybill = self).aggregate(Sum('amtpaid'))
        if(temp["amtpaid__sum"]):
            return temp["amtpaid__sum"]
        return 0

    def make_payment(self, Bvalue):
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
        if(Bvalue + self.paid_balance() > self.value):
            return self.paid_balance()
        payment.objects.create(mybill = self, amtpaid = Bvalue)
        return self.paid_balance()

    def delete(self):
        payment.objects.filter(mybill = self).delete()
        super(bill, self).delete()
