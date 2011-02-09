from django.db import models
from gus2.gus_users.models import gus_user
from gus2.gus_groups.models import gus_group
from django.db.models import Sum

class payment(models.Model):
    
    mybill = models.ForeignKey("bill")
    
    amtpaid = models.FloatField()
    datepaid = models.DateField(auto_now_add = True)

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


#COMMENT THIS!
    def paid_balance(self):
        temp = payment.objects.filter(mybill = self).aggregate(Sum('amtpaid'))
        return temp["amtpaid__sum"]

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
        payment.objects.create(mybill = self, amtpaid = Bvalue)
        return self.paid_balance()
    
    
    