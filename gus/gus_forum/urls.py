from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_forum.views', 
	(r"^<group_id>([0-9]+)/forums/$", 'forums'),
	(r"^<group_id>([0-9]+)/<forum_id>([0-9]+)/threads", 'threads'),
	(r"^<group_id>([0-9]+)/<forum_id>([0-9]+)/<thread_id>([0-9]+)/posts", 'posts'),
	(r"^<group_id>([0-9]+)/add_forum", 'add_forum'),
	(r"^<group_id>([0-9]+)/<forum_id>([0-9]+)/add_thread", 'add_thread'),
	(r"^<group_id>([0-9]+)/<forum_id>([0-9]+)/<thread_id>([0-9]6+)/add_post", 'add_thread'),)
