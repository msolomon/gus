from models import *
from django.contrib import admin

class gus_roleAdmin(admin.ModelAdmin):
	exclude=('name',)

class rolesInlines(admin.StackedInline):
	model=gus_roles
	extra=0
	exclude=('name',)

class gus_groupAdmin(admin.ModelAdmin):
#	def fieldset(self,request):
#		super(gus_groupAdmin, self).queryset(request).filter(gid__in = 'SELECT gid_id FROM gus_roles WHERE'

	inlines=[ rolesInlines ]
	
admin.site.register(gus_group,gus_groupAdmin)
admin.site.register(gus_user)
admin.site.register(gus_roles)

#Remove The Normal Group Management Interface
admin.site.unregister(User)
admin.site.unregister(Group)



