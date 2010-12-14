from django.db import models

# Create your models here.
cg=""
def current_group():return "find_group_name"
#ToDo implement methods to determin current group context
cm=""
def current_module():return "find_module_name"
#ToDo Implement methods to determine current module context
cr=""
def current_role():return "find_current_role"
#todo determin current role and permissions
	
class my_context(models.Model):
	context_group = current_group()
	context_module= current_module()
	context_role = current_role()
	
class gus_module(models.Model):
	module_name = models.CharField(max_length=100,unique=True)
	module_slug = models.CharField(max_length=100,unique=True)
	module_desc = models.TextField()
	authorized = models.BooleanField(null=True,blank=True)
