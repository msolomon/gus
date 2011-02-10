# Mike Solomon is to blame for content herein

from django.db import models
from django.core import mail
from gus2.gus_widget.models import Widget

from gus2.gus_groups.models import gus_group
from gus2.gus_users.models import gus_user

class EmailerWidget(Widget):
    '''
    The widget for managing emails within a group.
    '''
    # what else is needed besides the name (provided by Widget)?
    pass
    
class Emailer(models.Model):
    '''
    An email manager for a specific user
    '''
    user = models.ForeignKey(gus_user)
    groupies = [usr for usr in [grp for grp in user.getGroups()]]
    myaddress = models.CharField(max_length=128)
    myplaintextpassword = models.CharField(max_length=128)
    myusername = user.name
    
    def sendto_group(self, email):
        email.bcc = [usr.getEmail() for usr in groupies.getEmail()]
        email.send()

    def send_message(self, subject, message, recipient_list):
        mail.sendmassmail((subject, message, myemail, recipient_list))
