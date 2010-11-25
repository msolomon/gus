from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #just the welcome page
    (r'^(index.html)?$','gus.views.index'),
    #thanks for whatever
    (r'^thanks.html$','gus.views.thanks'),
    (r'^thanks/$','gus.views.thanks'),
    (r'^profile/$','gus.gus_groups.views.profile'),
    #register new user
    (r'^register.html$','gus.gus_groups.views.register'),
    (r'^register/$','gus.gus_groups.views.register'),
    #login existing user
    (r'^login.html$','gus.gus_groups.views.login'),
    (r'^login/$','gus.gus_groups.views.login'),


###(joran) gus_groups application views (manage users/groups/logins/etc)
    (r'^gus/', include('gus.gus_groups.urls')),

###(joran) gus_talk application views(forums)
    (r'^forums/', include('gus.gus_talk.urls')),

###(django)ADMIN VIEWS####
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/?', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/?', include(admin.site.urls)),
)
