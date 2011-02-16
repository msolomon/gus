from django.db import models
from gus2.gus_users.models import gus_user

# Create your models here.
class gus_backend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = gus_user.objects.get(_user__username=username)
            if user.check_password(password):
                return user
        except gus_user.DoesNotExist:
            return None


class AdminVars(models.Model):
    name=models.CharField(max_length=50)
    value=models.CharField(max_length=255)
