from models import *
from django.contrib import admin
from django import forms

admin.site.register(gus_user)
admin.site.register(gus_roles)

#Remove The Normal Group Management Interface
admin.site.unregister(User)
admin.site.unregister(Group)


class Roles_Inline(admin.StackedInline):
	model=gus_roles
	classes=['collapse']
	extra=1

class Gus_Group_Admin(admin.ModelAdmin):
	inlines=[Roles_Inline]
		

admin.site.register(gus_group,Gus_Group_Admin)


