from models import *
from django.contrib import admin
from django import forms

admin.site.register(gus_user)

#Remove The Normal Group Management Interface
admin.site.unregister(User)
admin.site.unregister(Group)




admin.site.register(gus_roles)



class Rform(forms.ModelForm):
	class Meta:
		model = gus_roles
		exclude = ('key',)
	
class Roles_Inline(admin.StackedInline):
	model=gus_roles
	form=Rform
	classes=['collapse']
	extra=0


class Gus_Group_Admin(admin.ModelAdmin):
	class Media:
		js=('js/collapsed_stacked_inlines.js',)
	inlines=[Roles_Inline]
		

admin.site.register(gus_group,Gus_Group_Admin)


