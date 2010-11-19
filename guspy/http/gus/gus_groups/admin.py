from models import *
from django.contrib import admin

admin.site.register(gus_group)
admin.site.register(gus_user)
admin.site.register(gus_roles)

#Remove The Normal Group Management Interface
admin.site.unregister(User)
admin.site.unregister(Group)



