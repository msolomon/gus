from django.db import models
from gus.gus_users.models import gus_user

# Create your models here.
class gus_backend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = gus_user.objects.get(_user__username=username)
            if user.check_password(password):
                return user
        except gus_user.DoesNotExist:
            return None
    def get_user(self,user_id):
        return gus_user.objects.get(pk=user_id)
    
    def get_all_permissions(self, user_obj):
        if user_obj.is_anonymous():
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in user_obj.user_permissions.select_related()])
            user_obj._perm_cache.update(self.get_group_permissions(user_obj))
        return user_obj._perm_cache


class AdminVars(models.Model):
    name=models.CharField(max_length=50)
    value=models.CharField(max_length=255)



    