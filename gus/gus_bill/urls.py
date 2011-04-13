
from django.conf.urls.defaults import *

urlpatterns = patterns('gus.gus_bill.views',
    (r'^(?P<group_id>[0-9]+)/$', 'index'),
    (r'^Add/(?P<group_id>[0-9]+)/$', 'AddBill'),
    (r'^Delete/(?P<bill_id>[0-9]+)/$', 'DeleteBill'),
    (r'^Payments/(?P<bill_id>[0-9]+)/$', 'Payments'),
    (r'^Archive/(?P<bill_id>[0-9]+)/$', 'Archive'),
)

