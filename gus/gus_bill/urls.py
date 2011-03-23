# GUS Gallery URLs
# Part of the GUSPY effort


from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_bill.views',
    (r'^$', 'index'),
    (r'^Add/$', 'AddBill'),
    (r'^Add/(?P<group_id>[0-9]+)/$', 'AddBill'),
)

