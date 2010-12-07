from django.contrib.auth.backends import *
from django.contrib.auth.models import *

class gus_custom_backend(ModelBackend):
	def get_grouprole_permissions(self, user_obj,group):
        	"""
        	Returns a set of permission strings that this user has 
		through his/her  grouprole.
        	"""
		_group_perm_cache=[]
        	if not hasattr(user_obj, '_group_perm_cache'):
			perms = Permission.objects.filter(gus_roles__uid=user_obj,gus_roles__gid=group
        	        	).values_list('content_type__app_label', 'codename'
                		).order_by()
			

			_group_perm_cache=set(["%s.%s" % (ct, name) for ct, name in perms])
        	return _group_perm_cache  
	def get_all_permissions(self,user_obj,group):
		return self.get_grouprole_permissions(user_obj,group)
	def get_group_permissions(self,user_obj,group):
		return self.get_grouprole_permissions(user_obj,group)

	def has_perm(self, user_obj, group,perm):
	        return perm in self.get_all_permissions(user_obj,group)

    	def has_module_perms(self, user_obj,group, app_label):
       		"""
        	Returns True if user_obj has any permissions in the given app_label.
        	"""                
        	for perm in self.get_all_permissions(user_obj,group):
            	  if perm[:perm.index('.')] == app_label:
                	return True
        	return False

	def group_role(self,user_obj,group_obj):
		"""returns gus_role of user for this group"""
		from gus.gus_groups.models import gus_roles
		try:
			return gus_roles.objects.get(uid=user_obj,gid=group_obj)
		except gus_roles.DoesNotExist:
			return None
