from models import *
from django.contrib import admin
from django import forms




	
class ForumAdmin(admin.ModelAdmin):
    pass

class ThreadAdmin(admin.ModelAdmin):
    list_display = ["_title", "_forum", "creator", "created"]
    list_filter = ["_forum", "creator"]

class PostAdmin(admin.ModelAdmin):
    search_fields = ["_title", "creator"]
    list_display = ["_title", "_thread", "creator", "created"]

admin.site.register(gus_forum, ForumAdmin)
admin.site.register(gus_thread, ThreadAdmin)
admin.site.register(gus_message, PostAdmin)


