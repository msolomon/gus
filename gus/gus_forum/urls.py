from django.conf.urls.defaults import *

urlpatterns = patterns("gus.gus_forum.views", 
	(r"^(?P<group_id>([0-9]+))/$", 'index'),
	(r"^(?P<group_id>([0-9]+))/add_forum/$", 'add_forum'),
	(r"^(?P<group_id>([0-9]+))/(?P<forum_id>([0-9]+))/$", 'view_threads'),
	(r"^(?P<group_id>([0-9]+))/(?P<forum_id>([0-9]+))/add_thread/$", 'add_thread'),
	(r"^(?P<group_id>([0-9]+))/(?P<forum_id>([0-9]+))/(?P<thread_id>([0-9]+))/$", 'view_posts'),
	(r"^(?P<group_id>([0-9]+))/(?P<forum_id>([0-9]+))/(?P<thread_id>([0-9]+))/add_post/$", 'add_post'),)
